# Example of a simple chatbot to csv

Folder structure
```bash
├───css
├───data: the actual files
├───exps: playground modules
├───resources: web resources
├───snapshots: screenshots
├───storage: the indexed data
```
No specific csv file format is required, but below is what verified good:

```text
name|price|url|description
Product Name|$39.98|https://the_url_is_replaced|product description
Product Name|$39.98|https://the_url_is_replaced|product description
```

## Prerequisites:
* create `.env` file with OPENAI API KEY:
    ```text
    OPENAI_API_KEY=your_key_here
    ```

Simply run:
```bash
streamlit run ui.py
```

## TODO:
* tailer prompt to suite use case
* remove lengthy prompt waste

