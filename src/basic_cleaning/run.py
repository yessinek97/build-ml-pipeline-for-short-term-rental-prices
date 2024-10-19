#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info(f"Input artifact downloaded and stored under: {artifact_local_path}")

    raw_df = pd.read_csv(artifact_local_path)

    # Drop outliers
    idx = (
        raw_df['price'].between(args.min_price, args.max_price) &
        raw_df['longitude'].between(-74.25, -73.50) &
        raw_df['latitude'].between(40.5, 41.2)
        )
    clean_df = raw_df[idx].copy()
    
    # Convert last_review to datetime
    clean_df['last_review'] = pd.to_datetime(clean_df['last_review'])

    logger.info("Data cleaning finished, logging artifact ...")


    clean_df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

    logger.info(f"Logged artifact with name {args.output_artifact}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="this step cleans the data")
    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="raw data input",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="cleaned data, output of the basic cleaning step",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="type of the output artifact",
        required=True
    )
    parser.add_argument(
        "--output_description", 
        type=str,
        help="description of the output artifact",
        required=True
    )
    parser.add_argument(
        "--min_price", 
        type=float,
        help="lower bound of the price value",
        required=True
    )
    parser.add_argument(
        "--max_price", 
        type=float,
        help="upper bound of the price value",
        required=True
    )

    args = parser.parse_args()

    go(args)
