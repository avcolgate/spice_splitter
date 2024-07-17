import os
import argparse
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_output_dir(output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f'Created output directory: {output_dir}')
    else:
        logging.info(f'Output directory already exists: {output_dir}')

def process_file(src_path: str, output_dir: str):
    subckt_section = False
    header = ""
    output = None
    name = ""

    with open(src_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if line.startswith(".GLOBAL") and not header:
                header = line
                logging.debug(f'Header found on line {line_num}: {header}')

            if line.startswith(".subckt") and not subckt_section:
                subckt_section = True
                name = line.split()[1]
                output_file_path = os.path.join(output_dir, f'{name}.typ.pex.netlist')
                output = open(output_file_path, 'w')
                output.write(f'{header}\n\n')
                logging.info(f'Started new subcircuit file: {output_file_path}')

            if line.startswith(".ends") and subckt_section and line.endswith(name):
                output.write(f'{line}\n')
                output.close()
                logging.info(f'Closed subcircuit file: {output.name}')
                subckt_section = False

            if subckt_section and output:
                output.write(f'{line}\n')

    logging.info("Split completed")

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Split netlist file into subcircuits.")
    parser.add_argument('src_path', type=str, help='Path to the source file')
    parser.add_argument('output_dir', type=str, help='Path to the output directory')
    args = parser.parse_args()

    ensure_output_dir(args.output_dir)
    process_file(args.src_path, args.output_dir)

if __name__ == "__main__":
    main()
