#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    # Initialize a W&B run
    logger.info("Initializing W&B run for basic cleaning")
    run = wandb.init(
        project="nyc_airbnb",
        job_type="basic_cleaning"
    )
    
    # Update the run configuration with the provided arguments
    logger.info("Updating run configuration with provided arguments")
    run.config.update(args)



    # Load the dataset
    logger.info(f"Loading dataset from {args.input_artifact}")
    artifact_local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    

    # Filter the dataset based on price
    logger.info(f"Filtering dataset with min_price={args.min_price} and max_price={args.max_price}")
    df = df[(df['price'] >= args.min_price) & (df['price'] <= args.max_price)]

    # Remove rows outside the proper geolocation range
    logger.info("Removing rows with invalid geolocation")
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    
    # Save the cleaned dataset to a new artifact
    output_path = args.output_artifact
    logger.info(f"Saving cleaned dataset to {output_path}")
    df.to_csv(output_path, index=False)

    # Log the output artifact
    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description        
    )
    artifact.add_file(output_path)
    run.log_artifact(artifact)

    run.finish()

    logger.info("Basic cleaning completed successfully.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Path to the input artifact containing the raw listings data, e.g., sample.csv.",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Path to the output artifact where the cleaned listings data will be stored, e.g., clean_sample.csv.",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the output artifact. This should match the expected format for the cleaned data, e.g., clean_sample.",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the output artifact, providing context about the cleaned data.",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to filter listings. Listings with a price below this value will be removed.",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price to filter listings. Listings with a price above this value will be removed.",
        required=True
    )


    args = parser.parse_args()

    go(args)
