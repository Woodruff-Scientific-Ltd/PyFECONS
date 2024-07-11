import argparse
import os

import pandas as pd

from utils import save_capacity_change_graph


def main(input_csv, start_year, end_year, out_dir, filename):
    output_file = os.path.join(out_dir, filename)
    print(f'Plotting capacity change for {input_csv} and saving to {output_file}')
    os.makedirs(out_dir, exist_ok=True)

    simulation_results = pd.read_csv(input_csv)

    save_capacity_change_graph(simulation_results, start_year, end_year, output_file)
    print('Capacity plot saved')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot capacity change graph for simulation output")
    parser.add_argument('--input_csv', type=str, default="out/run/simulation_summary.csv",
                        help="Simulation results csv file.")
    parser.add_argument('--out_dir', type=str, default="out/run", help="Output directory to save file")
    parser.add_argument('--filename', type=str, default="capacity_graph.png", help="Output directory to save file")
    parser.add_argument('--start_year', type=int, default=None, help="Start year of graph")
    parser.add_argument('--end_year', type=int, default=None, help="End year of graph")

    args = parser.parse_args()

    main(args.input_csv, args.start_year, args.end_year, args.out_dir, args.filename)
