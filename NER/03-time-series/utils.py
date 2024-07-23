import spacy
from spacy.tokens.doc import Doc
from spacy.tokens import DocBin
def convert_jsonl_to_docbin(input_file, output_file, model="en_core_web_trf", relation_labels=[]):
    """
    Convert JSONL file to Spacy DocBin file.

    Args:
        input_file (str): Path to the input JSONL file.
        output_file (str): Path to save the output DocBin file.
        model (str, optional): Spacy model to use. Defaults to "en_core_web_trf".
        relation_labels (list, optional): List of relation labels. Defaults to an empty list.
    """

    # Load Spacy model
    nlp = spacy.load(model)

    # Read JSONL file
    annotations = pd.read_json(input_file, lines=True)

    # Set extension for Doc object
    Doc.set_extension("rel", default={}, force=True)

    # Create DocBin object to store processed documents
    db = DocBin()

    # List to store IDs with issues
    ids_with_issues = []

    # Iterate over each annotation in the JSONL file
    for index, row in annotations.iterrows():
        try:
            span_starts = set()
            entities = []
            span_end_to_start = {}

            # Get text from the annotation
            print("ID: {}".format(row["id"]))
            text = row["text"]

            # Create a Doc object from the text using the Spacy model
            doc = nlp.make_doc(text)

            # Keep track of referenced entities to avoid duplicates
            ref_entities = []

            # Process each entity in the annotation
            for entity in row["entities"]:
                start = entity["start_offset"]
                end = entity["end_offset"]

                # Check if the entity has not been referenced before
                if (start, end) not in ref_entities:
                    ref_entities.append((start, end))
                    label = entity["label"]

                    # Create a span from the character offsets and label
                    span = doc.char_span(start, end, label=label)

                    if span is None:
                        print("Skipping entity for {0} {1} - Offset ({1},{2})".format(label, start, end))
                    else:
                        entities.append(span)
                        span_end_to_start[entity["id"]] = entity["id"]
                        span_starts.add(entity["id"])

            # Create an empty dictionary to store relations
            rels = {}
            for x1 in span_starts:
                for x2 in span_starts:
                    rels[(x1, x2)] = {}

            # Process relations in the annotation
            relations = row.get("relations", [])  # Use an empty list if 'relations' key is missing
            for relation in relations:
                start = span_end_to_start.get(relation["from_id"], None)  # Set None if 'from_id' key is missing
                end = span_end_to_start.get(relation["to_id"], None)  # Set None if 'to_id' key is missing
                label = relation["type"]

                if start is not None and end is not None:
                    if label not in rels[(start, end)]:
                        rels[(start, end)][label] = 1.0

                # Fill in zeros where relation data is missing
                for x1 in span_starts:
                    for x2 in span_starts:
                        for label in relation_labels:
                            if label not in rels[(x1, x2)]:
                                rels[(x1, x2)][label] = 0.0

            # Assign the entities and relations to the Doc object
            doc.ents  = entities
            doc._.rel = rels

            # Add the processed document to the DocBin object
            db.add(doc)

        except Exception as e:
            print(f"Error processing ID {row['id']}: {str(e)}")
            ids_with_issues.append(row["id"])

    # Save the DocBin object to disk
    db.to_disk(output_file)

    return db, ids_with_issues