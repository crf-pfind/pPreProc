#ifndef PPREPROC_PFB_READER_HPP
#define PPREPROC_PFB_READER_HPP

#include <algorithm>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace ppreproc {

/// Error raised when a PFB/PFC pair violates the documented v1 contract.
class pfb_format_error : public std::runtime_error {
 public:
  using std::runtime_error::runtime_error;
};

/// Decoded spectrum record and the matching PFC metadata row.
struct spectrum_record {
  /// Zero-based record ordinal.
  std::size_t index{};
  /// Absolute PFB byte boundaries for the record.
  std::uint64_t start_pos{};
  std::uint64_t end_pos{};
  /// UTF-8 property string stored in PFB.
  std::string property_text;
  /// Double-precision peak arrays; empty for metadata-only access.
  std::vector<double> mz;
  std::vector<double> intensity;
  /// PFC values keyed by column name.
  std::unordered_map<std::string, std::string> metadata;
};

/// Indexed reader for a PFB file and its PFC companion.
class pfb_reader {
 public:
  /// Open and structurally validate a PFB/PFC v1 pair.
  ///
  /// When `pfc_path` is empty, the same-stem `.pfc` path is selected.
  explicit pfb_reader(const std::string& pfb_path, std::string pfc_path = {})
      : pfb_path_(pfb_path),
        pfc_path_(pfc_path.empty() ? default_pfc_path(pfb_path_)
                                   : std::move(pfc_path)),
        input_(pfb_path_, std::ios::binary) {
    if (!input_) throw pfb_format_error("cannot open PFB file");
    input_.seekg(0, std::ios::end);
    file_size_ = checked_position(input_.tellg());
    if (file_size_ < header_size) {
      throw pfb_format_error("PFB is smaller than its 24-byte v1 header");
    }
    input_.seekg(0);
    reserved_[0] = read_i32();
    reserved_[1] = read_i32();
    reserved_[2] = read_i32();
    index_address_ = read_u64();
    const auto signed_count = read_i32();
    if (signed_count < 0) throw pfb_format_error("negative spectrum count");
    spectrum_count_ = static_cast<std::size_t>(signed_count);
    read_index();
    read_pfc();
    validate_structure();
  }

  /// Return the number of spectra.
  std::size_t size() const noexcept { return spectrum_count_; }
  /// Return the absolute offset of the footer index.
  std::uint64_t index_address() const noexcept { return index_address_; }
  /// Return the resolved PFB path.
  const std::string& pfb_path() const noexcept { return pfb_path_; }
  /// Return the resolved PFC path.
  const std::string& pfc_path() const noexcept { return pfc_path_; }

  /// Retrieve a record by zero-based ordinal through the footer index.
  ///
  /// Set `with_arrays` to false for metadata-only access.
  spectrum_record spectrum(std::size_t index, bool with_arrays = true) {
    if (index >= spectrum_count_) throw std::out_of_range("spectrum index");
    const auto start = offsets_[index];
    const auto end = index + 1 < spectrum_count_ ? offsets_[index + 1]
                                                 : index_address_;
    input_.clear();
    input_.seekg(static_cast<std::streamoff>(start));
    const auto property_size = read_u32();
    if (property_size > end - start) {
      throw pfb_format_error("property string exceeds record boundary");
    }
    std::string property(property_size, '\0');
    read_exact(property.data(), property.size());
    if (!property.empty() && property.back() == '\0') property.pop_back();
    const auto peak_count = read_u32();
    const auto remaining = end - checked_position(input_.tellg());
    if (peak_count > std::numeric_limits<std::uint64_t>::max() / 16 ||
        remaining != static_cast<std::uint64_t>(peak_count) * 16) {
      throw pfb_format_error("peak arrays do not match record boundary");
    }
    std::vector<double> mz;
    std::vector<double> intensity;
    if (with_arrays) {
      mz.reserve(peak_count);
      intensity.reserve(peak_count);
      for (std::uint32_t i = 0; i < peak_count; ++i) mz.push_back(read_f64());
      for (std::uint32_t i = 0; i < peak_count; ++i)
        intensity.push_back(read_f64());
    } else {
      input_.seekg(static_cast<std::streamoff>(remaining), std::ios::cur);
    }
    const auto metadata = metadata_rows_[index];
    if (required_u64(metadata, "NumberofPeaks") != peak_count)
      throw pfb_format_error("PFC/PFB peak-count mismatch");
    if (required_u64(metadata, "StartPos") != start ||
        required_u64(metadata, "EndPos") != end)
      throw pfb_format_error("PFC/PFB byte-boundary mismatch");
    return {index, start, end, std::move(property), std::move(mz),
            std::move(intensity), std::move(metadata)};
  }

  /// Retrieve a record using its PFC `ScanNo` identifier.
  spectrum_record spectrum_by_scan(const std::string& scan,
                                   bool with_arrays = true) {
    const auto found = scan_to_index_.find(scan);
    if (found == scan_to_index_.end()) throw std::out_of_range("unknown ScanNo");
    return spectrum(found->second, with_arrays);
  }

  /// Follow PFC parent links until the corresponding MS1 is reached.
  spectrum_record parent_ms1(const spectrum_record& child,
                             bool with_arrays = true) {
    auto parent = field(child.metadata, "PrecursorScan");
    if (parent.empty()) throw pfb_format_error("spectrum has no parent scan");
    std::vector<std::string> visited;
    while (true) {
      if (std::find(visited.begin(), visited.end(), parent) != visited.end())
        throw pfb_format_error("cycle in parent-scan links");
      visited.push_back(parent);
      auto candidate = spectrum_by_scan(parent, false);
      if (upper(field(candidate.metadata, "SpectrumType")) == "MS1") {
        return with_arrays ? spectrum(candidate.index, true) : candidate;
      }
      parent = field(candidate.metadata, "PrecursorScan");
      if (parent.empty()) throw pfb_format_error("non-MS1 parent has no parent");
    }
  }

 private:
  static constexpr std::uint64_t header_size = 24;

  static std::string default_pfc_path(const std::string& path) {
    const auto separator = path.find_last_of("/\\");
    const auto extension = path.find_last_of('.');
    const auto stem_end = extension != std::string::npos &&
                                  (separator == std::string::npos ||
                                   extension > separator)
                              ? extension
                              : path.size();
    return path.substr(0, stem_end) + ".pfc";
  }

  std::string pfb_path_;
  std::string pfc_path_;
  std::ifstream input_;
  std::uint64_t file_size_{};
  std::int32_t reserved_[3]{};
  std::uint64_t index_address_{};
  std::size_t spectrum_count_{};
  std::vector<std::uint64_t> offsets_;
  std::vector<std::unordered_map<std::string, std::string>> metadata_rows_;
  std::unordered_map<std::string, std::size_t> scan_to_index_;

  static std::uint64_t checked_position(std::streampos position) {
    if (position < 0) throw pfb_format_error("invalid file position");
    return static_cast<std::uint64_t>(position);
  }

  void read_exact(char* target, std::size_t count) {
    if (!count) return;
    input_.read(target, static_cast<std::streamsize>(count));
    if (input_.gcount() != static_cast<std::streamsize>(count))
      throw pfb_format_error("unexpected end of PFB file");
  }

  std::uint64_t read_unsigned(std::size_t count) {
    unsigned char bytes[8]{};
    read_exact(reinterpret_cast<char*>(bytes), count);
    std::uint64_t result = 0;
    for (std::size_t i = 0; i < count; ++i)
      result |= static_cast<std::uint64_t>(bytes[i]) << (8 * i);
    return result;
  }

  std::uint32_t read_u32() {
    return static_cast<std::uint32_t>(read_unsigned(4));
  }
  std::uint64_t read_u64() { return read_unsigned(8); }
  std::int32_t read_i32() {
    const auto value = read_u32();
    std::int32_t result{};
    std::memcpy(&result, &value, sizeof(result));
    return result;
  }
  double read_f64() {
    const auto bits = read_u64();
    double result{};
    std::memcpy(&result, &bits, sizeof(result));
    return result;
  }

  void read_index() {
    if (index_address_ < header_size || index_address_ > file_size_)
      throw pfb_format_error(
          "invalid footer index address; unsupported legacy or corrupt PFB");
    if (file_size_ - index_address_ != spectrum_count_ * 8)
      throw pfb_format_error("footer index size mismatch");
    input_.seekg(static_cast<std::streamoff>(index_address_));
    offsets_.reserve(spectrum_count_);
    for (std::size_t i = 0; i < spectrum_count_; ++i)
      offsets_.push_back(read_u64());
  }

  static std::vector<std::string> split_tsv(const std::string& line) {
    std::vector<std::string> fields;
    std::size_t start = 0;
    while (true) {
      const auto tab = line.find('\t', start);
      fields.push_back(line.substr(start, tab - start));
      if (tab == std::string::npos) break;
      start = tab + 1;
    }
    return fields;
  }

  void read_pfc() {
    std::ifstream pfc(pfc_path_);
    if (!pfc) throw pfb_format_error("missing companion PFC file");
    std::string line;
    if (!std::getline(pfc, line)) throw pfb_format_error("PFC has no header");
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.size() >= 3 && static_cast<unsigned char>(line[0]) == 0xEF &&
        static_cast<unsigned char>(line[1]) == 0xBB &&
        static_cast<unsigned char>(line[2]) == 0xBF)
      line.erase(0, 3);
    const auto headers = split_tsv(line);
    const std::vector<std::string> required_headers = {
        "ScanNo",          "PrecursorScan",   "RetTime",
        "SpectrumType",    "InstrumentType", "IonInjectionTime",
        "activationType",  "activationCenter", "NCE",
        "monoIsotopicMz",  "upperCharge",    "lowerCharge",
        "activationWindow", "NumberofPeaks", "StartPos",
        "EndPos"};
    for (const auto& required : required_headers)
      if (std::find(headers.begin(), headers.end(), required) == headers.end())
        throw pfb_format_error("PFC is missing v1 column: " + required);
    while (std::getline(pfc, line)) {
      if (!line.empty() && line.back() == '\r') line.pop_back();
      const auto values = split_tsv(line);
      std::unordered_map<std::string, std::string> row;
      for (std::size_t i = 0; i < headers.size(); ++i)
        row[headers[i]] = i < values.size() ? values[i] : "";
      const auto scan = field(row, "ScanNo");
      if (scan.empty()) throw pfb_format_error("PFC row has no ScanNo");
      if (!scan_to_index_.emplace(scan, metadata_rows_.size()).second)
        throw pfb_format_error("duplicate PFC ScanNo");
      metadata_rows_.push_back(std::move(row));
    }
  }

  void validate_structure() const {
    if (metadata_rows_.size() != spectrum_count_)
      throw pfb_format_error("PFB spectrum count and PFC row count differ");
    if (!spectrum_count_) {
      if (index_address_ != header_size)
        throw pfb_format_error("empty PFB has a data region");
      return;
    }
    if (offsets_.front() != header_size)
      throw pfb_format_error("first record does not begin after header");
    for (std::size_t i = 1; i < offsets_.size(); ++i)
      if (offsets_[i - 1] >= offsets_[i])
        throw pfb_format_error("record offsets are not strictly increasing");
    if (offsets_.back() >= index_address_)
      throw pfb_format_error("last record begins outside data region");
  }

  static std::string field(
      const std::unordered_map<std::string, std::string>& row,
      const std::string& name) {
    const auto found = row.find(name);
    return found == row.end() ? std::string{} : found->second;
  }

  static std::uint64_t required_u64(
      const std::unordered_map<std::string, std::string>& row,
      const std::string& name) {
    const auto value = field(row, name);
    if (value.empty()) throw pfb_format_error("empty PFC field: " + name);
    try {
      std::size_t consumed = 0;
      const auto parsed = std::stoull(value, &consumed);
      if (consumed != value.size())
        throw pfb_format_error("invalid PFC field: " + name);
      return parsed;
    } catch (const pfb_format_error&) {
      throw;
    } catch (const std::exception&) {
      throw pfb_format_error("invalid PFC field: " + name);
    }
  }

  static std::string upper(std::string value) {
    for (auto& character : value)
      if (character >= 'a' && character <= 'z') character -= ('a' - 'A');
    return value;
  }
};

}  // namespace ppreproc

#endif
