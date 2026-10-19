import argparse
from pathlib import Path
from app.services.document_service import DocumentService
from uuid import UUID
def main() -> None:
    parser = argparse.ArgumentParser(description="Document Processing Service")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser('add', help='Add a new document')
    add_parser.add_argument('file_path', type=Path, help='Path to the document file')

    list_parser = subparsers.add_parser('list', help='List all of documents')

    get_parser = subparsers.add_parser('get', help='Get documnet')
    get_parser.add_argument('document_id', type=UUID, help='Document ID')

    delete_parser = subparsers.add_parser('delete', help='Delete Document', aliases=['del', 'rm'])
    delete_parser.add_argument('document_id', type=UUID, help='Document ID')

    args = parser.parse_args()

    service = DocumentService()

    try:
        if args.command == 'add':
            document_id = service.create_document(args.file_path)
            print(f"document created successfully: {document_id}")
        if args.command == 'list':
            documents = service.list_documents()
            headers = ("ID" , "FILENAME", "SIZE", "WORDS")

            print(
                f"{headers[0]:^36}|"
                f"{headers[1]:^25}|"
                f"{headers[2]:^10}|"
                f"{headers[3]:^10}|"
            )
            print("-" * 87)
            for document in documents:
                print(
                    f"{document['id']:^36}|"
                    f"{document['filename']:^25}|"
                    f"{document['size']:^10}|"
                    f"{document['word_count']:^10}|"
                )
        if args.command == 'get':
            document = service.get_document(args.document_id)

            print("Document Details")
            print("-" * 40)
            print(f"ID:          {document['id']}")
            print(f"Filename:    {document['filename']}")
            print(f"Size:        {document['size']} bytes")
            print(f"Word Count:  {document['word_count']}")
            print(f"Status:      {document['status']}")
            print(f"Created At:  {document['created_at']}")
        if args.command in ['delete' , 'rm' , 'del']:
            service.delete_document(args.document_id)
            print(f"Document deleted successfully: {args.document_id}")
    except FileNotFoundError as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")



if __name__ == '__main__':
    main()