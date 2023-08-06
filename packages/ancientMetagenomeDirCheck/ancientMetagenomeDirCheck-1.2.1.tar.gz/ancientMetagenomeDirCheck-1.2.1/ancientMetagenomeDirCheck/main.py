import pandas as pd
import json
from jsonschema import Draft7Validator
from io import StringIO
from ancientMetagenomeDirCheck.exceptions import DatasetValidationError, DuplicateError, ColumnDifferenceError
import sys
from rich import print
from rich.console import Console
from rich.table import Table


def check_extra_missing_columns(dataset, schema):
    """Check if there are extra or missing column in dataset

    Args:
        dataset (str): Path to dataset in tsv format
        schema (str): path to json schema
    Raises:
        ColumnDifferenceError: If dataset has extra or missing columns compared to schema
    """    

    dt = pd.read_csv(dataset, sep="\t")
    dt_json = json.load((StringIO(dt.to_json(orient="records"))))

    with open(schema, "r") as j:
        json_schema = json.load(j)

    required_columns = json_schema['items']['required']
    present_columns = list(dt.columns)
    missing_columns = list(set(required_columns) - set(present_columns))
    extra_columns = list(set(present_columns) - set(required_columns))
    if len(missing_columns) > 0:
        message = f"The required column(s) {', '.join(missing_columns)} is/are missing"
        raise ColumnDifferenceError(message)
    if len(extra_columns) > 0:
        message = f"Additional column(s) {', '.join(extra_columns)} not allowed"
        raise ColumnDifferenceError(message)



def check_validity(dataset, schema):
    """Check validity of dataset against schema

    Args:
        dataset (str): Path to dataset in tsv format
        schema (str): path to json schema
    Raises:
        DatasetValidationError: If dataset is not validated by schema

    """
    dt = pd.read_csv(dataset, sep="\t")
    dt_json = json.load((StringIO(dt.to_json(orient="records"))))

    with open(schema, "r") as j:
        json_schema = json.load(j)

    v = Draft7Validator(json_schema)
    errors = []
    for error in sorted(v.iter_errors(dt_json), key=str):
        errors.append(error)
    if len(errors) > 0:
        table = Table(title="Validation Errors were found")
        table.add_column("Offending value", justify="right", style="red", no_wrap=True)
        table.add_column("Line number", style="red")
        table.add_column("Column", justify="right", style="cyan")
        table.add_column("Error", style="magenta")
        lines = []
        for error in errors:
            err_column = list(error.path)[-1]
            if "enum" in error.schema:
                if len(error.schema["enum"]) > 3:
                    error.message = f"'{error.instance}' is not an accepted value.\nPlease check {json_schema['items']['properties'][err_column]['$ref']}"
            err_line = str(error.path[0]+2)
            lines.append(
                [str(error.instance), err_line, str(err_column), error.message]
            )

        # remove duplicate lines
        b_set = set(tuple(x) for x in lines)
        b = [list(x) for x in b_set]

        for l in b:
            table.add_row(*l)
        console = Console()
        console.print(table)

        raise (DatasetValidationError("DatasetValidationError"))


def check_duplicates(dataset):
    """Check for rows duplicatations

    Args:
        dataset (str): Path to dataset in tsv format
    Raises:
        DuplicateError: If duplicate lines are found

    """
    dt = pd.read_csv(dataset, sep="\t")
    if dt.duplicated().sum() != 0:
        message = f"Duplication Error\n{dt[dt.duplicated()]} line is duplicated"
        raise (DuplicateError(message))


def check_accession_duplicates(dataset):
    """Check for duplicates in sample accession numbers

    Args:
        dataset (str): Path to dataset in tsv format
    Raises:
        DuplicateError: If accessions duplicates are found
    """
    accessions_raw = pd.read_csv(dataset, sep="\t")["archive_accession"]
    accessions = [
        entry for acc in accessions_raw.dropna().tolist() for entry in acc.split(",")
    ]
    # Checking for duplicated entries
    if len(list(set(accessions))) != len(accessions):
        duplicated = []
        for acc in accessions:
            if accessions.count(acc) > 1:
                duplicated.append(acc)
        # Getting duplicated accessions numbers
        duplicated = list(set(duplicated))

        # Getting the line numbers of duplicated entries
        duplicate_entries = {}
        all_accessions_raw = accessions_raw.to_list()
        for acc in duplicated:
            for nb, entry in enumerate(all_accessions_raw):
                if str(acc) in str(entry):
                    if str(acc) not in duplicate_entries:
                        duplicate_entries[acc] = [nb + 2]
                    else:
                        duplicate_entries[acc].append(nb + 2)

        table = Table(title="Duplicate accessions numbers were found")
        table.add_column(
            "Accession number", justify="right", style="cyan", no_wrap=True
        )
        table.add_column("Line", style="magenta")
        table.add_column("Column", style="red")
        for acc in duplicate_entries:
            table.add_row(
                acc,
                ", ".join([str(i) for i in duplicate_entries[acc]]),
                "archive_accession",
            )
        console = Console()
        console.print(table)
        message = "DuplicateAccessionError"

        raise (DuplicateError(message))


def run_tests(dataset, schema, validity, duplicate, accession):
    try:
        check_extra_missing_columns(dataset, schema)
        if not duplicate:
            check_duplicates(dataset)
        if not accession:
            check_accession_duplicates(dataset)
        if not validity:
            check_validity(dataset, schema)
        print("[green]All is good, no errors were found ![/green]")
    except (DatasetValidationError, DuplicateError, ColumnDifferenceError) as e:
        print(f"[red]{e}[/red]")
        sys.exit(1)
