import yaml


def main():
    CONFIG = yaml.load(open('config_global.yaml', 'r'), Loader = yaml.SafeLoader)
    with open('%s/data.txt' % CONFIG['build']['prepare_data'], 'w') as f:
        f.write('x\n')
        f.writelines(['%s\n' % x for x in range(1, 300001)])

main()
