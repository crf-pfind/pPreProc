#include <iomanip>
#include <iostream>

#include "ppreproc/pfb_reader.hpp"

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: read_pfb <file.pfb>\n";
    return 2;
  }
  try {
    ppreproc::pfb_reader reader(argv[1]);
    const auto record = reader.spectrum_by_scan("102");
    const auto parent = reader.parent_ms1(record);
    std::cout << "spectra=" << reader.size() << "\n"
              << "scan=102 peaks=" << record.mz.size() << " first_mz="
              << std::fixed << std::setprecision(1) << record.mz.front() << "\n"
              << "parent_scan=" << parent.metadata.at("ScanNo") << "\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "PFB/PFC error: " << error.what() << "\n";
    return 1;
  }
}
