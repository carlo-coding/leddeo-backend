import argostranslate.package
import argostranslate.translate

def download_packages(from_code, to_code):
  argostranslate.package.update_package_index()
  try:
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = list(
      filter(
          lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
      )
    )
    if (len(package_to_install) != 0): 
      argostranslate.package.install_from_path(package_to_install[0].download())
    else:
      for package_one in available_packages:
        if (package_one.from_code != from_code):
          continue
        package_two = list(
          filter(
              lambda x: x.from_code == package_one.to_code and x.to_code == to_code, available_packages
          )
        )
        if (len(package_two) != 0):
          break
      package_one.code
      if (package_one and package_two):
        print(f"from {package_one.from_name} to {package_one.to_name} to {package_two[0].to_name}")
        argostranslate.package.install_from_path(package_one.download())
        argostranslate.package.install_from_path(package_two[0].download())
        return [from_code, package_one.to_code, to_code]
      else:
        return []

    return [from_code, to_code]
  except:
    print(f"Error inpackage download {from_code} to {to_code}")
    return []