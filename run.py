"""
Resume Parser - Main Entry Point

This script processes all resume PDFs in the data/raw_resumes directory
and generates a structured CSV output with parsed information.

Usage:
    python run.py                    # Run with default settings
    python run.py --debug           # Run with debug logging
    python run.py --input <dir>     # Specify input directory
    python run.py --output <file>   # Specify output file
"""

import os
import sys
import argparse
import logging
import pandas as pd
from typing import List, Dict, Any

from config import INPUT_DIR, OUTPUT_DIR, OUTPUT_FILE, LOG_LEVEL, LOG_FORMAT
from src.pipeline import process_resume

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "logs", "resume_parser.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Resume Parser - Extract structured data from PDF resumes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                          # Process all PDFs in data/raw_resumes/
  python run.py --debug                  # Enable debug logging
  python run.py --input path/to/resumes  # Specify custom input directory
  python run.py --output results.csv     # Specify custom output file
        """
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=INPUT_DIR,
        help=f"Input directory with PDF resumes (default: {INPUT_DIR})"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=OUTPUT_FILE,
        help=f"Output CSV filename (default: {OUTPUT_FILE})"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=OUTPUT_DIR,
        help=f"Output directory for CSV file (default: {OUTPUT_DIR})"
    )
    
    return parser.parse_args()


def validate_input_directory(input_dir: str) -> bool:
    """
    Validate that input directory exists and contains PDF files.
    
    Args:
        input_dir (str): Path to input directory.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    if not os.path.exists(input_dir):
        logger.error(f"Input directory does not exist: {input_dir}")
        return False
    
    if not os.path.isdir(input_dir):
        logger.error(f"Input path is not a directory: {input_dir}")
        return False
    
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return True  # Still valid, just no files to process
    
    logger.info(f"Found {len(pdf_files)} PDF file(s) to process")
    return True


def process_resumes(input_dir: str) -> List[Dict[str, Any]]:
    """
    Process all PDFs in the input directory.
    
    Args:
        input_dir (str): Path to directory containing resume PDFs.
        
    Returns:
        List[Dict[str, Any]]: List of parsed resume data dictionaries.
    """
    results = []
    failed_files = []
    
    if not os.path.exists(input_dir):
        logger.error(f"Input directory not found: {input_dir}")
        return results
    
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    total_files = len(pdf_files)
    
    if total_files == 0:
        logger.warning(f"No PDF files found in {input_dir}")
        return results
    
    logger.info(f"Starting batch processing of {total_files} resume(s)...")
    
    for idx, filename in enumerate(pdf_files, 1):
        try:
            pdf_path = os.path.join(input_dir, filename)
            logger.info(f"[{idx}/{total_files}] Processing: {filename}")
            
            data = process_resume(pdf_path)
            
            if data:
                results.append(data)
                logger.debug(f"✓ Successfully processed: {filename}")
            else:
                failed_files.append(filename)
                logger.warning(f"✗ Failed to extract data from: {filename}")
                
        except Exception as e:
            failed_files.append(filename)
            logger.error(f"✗ Error processing {filename}: {str(e)}", exc_info=True)
    
    # Log summary
    logger.info("=" * 60)
    logger.info(f"Processing Summary:")
    logger.info(f"  Total files: {total_files}")
    logger.info(f"  Successfully processed: {len(results)}")
    logger.info(f"  Failed: {len(failed_files)}")
    
    if failed_files:
        logger.warning(f"Failed files: {', '.join(failed_files)}")
    
    logger.info("=" * 60)
    
    return results


def save_results(results: List[Dict[str, Any]], output_dir: str, output_file: str) -> bool:
    """
    Save parsed results to CSV file.
    
    Args:
        results (List[Dict]): List of parsed resume data.
        output_dir (str): Output directory path.
        output_file (str): Output filename.
        
    Returns:
        bool: True if save successful, False otherwise.
    """
    try:
        if not results:
            logger.warning("No results to save")
            return False
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        
        # Ensure Skills column is string type (for CSV compatibility)
        if 'Skills' in df.columns:
            df['Skills'] = df['Skills'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        
        output_path = os.path.join(output_dir, output_file)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        
        logger.info(f"✓ Results saved to: {output_path}")
        logger.info(f"  Records: {len(df)}")
        logger.info(f"  Columns: {', '.join(df.columns)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}", exc_info=True)
        return False


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set logging level
        if args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")
        
        # Handle case where output includes directory path
        output_file = os.path.basename(args.output)
        output_dir = args.output_dir
        if "/" in args.output or "\\" in args.output:
            output_dir = os.path.dirname(args.output)
            if not output_dir:
                output_dir = args.output_dir
        
        logger.info("Resume Parser - Starting Batch Processing")
        logger.info(f"Input directory: {args.input}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Output file: {output_file}")
        
        # Validate input
        if not validate_input_directory(args.input):
            logger.error("Input validation failed")
            sys.exit(1)
        
        # Process resumes
        results = process_resumes(args.input)
        
        # Save results
        if results:
            if save_results(results, output_dir, output_file):
                logger.info("✓ Batch processing completed successfully")
                sys.exit(0)
            else:
                logger.error("✗ Failed to save results")
                sys.exit(1)
        else:
            logger.warning("No results to save")
            sys.exit(0)
    
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

