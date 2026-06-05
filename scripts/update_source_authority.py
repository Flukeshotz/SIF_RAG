from db.qdrant_connection import get_client
from qdrant_client.models import PointStruct

def get_mapping(document_type, document_id):
    doc_id_lower = document_id.lower()
    
    # Infer doc_type if unknown
    if document_type == "Unknown" or not document_type:
        if "sebi-circular" in doc_id_lower: document_type = "SEBI Circular"
        elif "amfi-circular" in doc_id_lower: document_type = "AMFI Circular"
        elif "isid" in doc_id_lower: document_type = "ISID"
        elif "kim" in doc_id_lower: document_type = "KIM"
        elif "factsheet" in doc_id_lower: document_type = "Factsheet"
    
    if document_type in ["SEBI Circular", "AMFI Circular"]:
        return 1, "regulator", document_type
    elif document_type in ["ISID", "KIM", "Factsheet", "Factsheets"]:
        return 2, "official_amc", document_type
    elif document_type == "Webpage":
        if "groww.in" in doc_id_lower:
            return 4, "aggregator", document_type
        elif "indmoney.com" in doc_id_lower:
            return 4, "aggregator", document_type
        elif "blog" in doc_id_lower:
            return 5, "blog", document_type
        else:
            return 3, "official_amc", document_type
    else:
        # Default fallback
        return 3, "official_amc", document_type

def main():
    print("Updating Source Authority in Qdrant...")
    client = get_client()
    collection_name = "sif_documents"
    
    # Retrieve all points (assuming we have ~2500, we can fetch all by scrolling)
    points_to_update = []
    
    offset = None
    total_processed = 0
    
    while True:
        # scroll returns (points, next_page_offset)
        res = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False # we don't need vectors just to update payload
        )
        points, offset = res
        
        for point in points:
            payload = point.payload
            doc_type = payload.get("document_type", "Unknown")
            doc_id = payload.get("document_id", "")
            
            tier, auth, new_doc_type = get_mapping(doc_type, doc_id)
            
            # Note: qdrant set_payload merges into the existing payload
            client.set_payload(
                collection_name=collection_name,
                payload={
                    "priority_tier": tier,
                    "source_authority": auth,
                    "document_type": new_doc_type
                },
                points=[point.id]
            )
            total_processed += 1
            
        if offset is None:
            break
            
    print(f"Successfully updated metadata for {total_processed} vectors.")

if __name__ == "__main__":
    main()
