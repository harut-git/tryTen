f = open('base_config.reg', 'r')
lines = f.readlines()
new_lines = lines
for i in range(0, len(lines)):
    if lines[i] == "[-HKEY_CURRENT_USER\Software\Zero]\n":
        new_lines.insert(i+1, "Hello\n")
        new_lines.insert(i+1, "bye\n")
        print("ok")
k = open('generated.reg', 'w+')
k.writelines(new_lines)
print(new_lines)