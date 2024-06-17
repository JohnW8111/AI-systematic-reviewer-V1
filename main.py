#you need to pip install the following libraries anthropic and pypdf
# you need to have an anthropic api key

import os
import pypdf
import anthropic


# Create a directory to store PDFs
pdf_directory = 'pdfs'
os.makedirs(pdf_directory, exist_ok=True)

# Function to merge PDFs and save the content as a text file
def merge_pdfs_to_text(pdf_folder, output_text_file):

    all_text = ''

    # Iterate over all the PDF files in the directory
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_reader = pypdf.PdfReader(pdf_path)

            # Extract text from each page and add it to the all_text variable
            for page_num in range(len(pdf_reader.pages)):
               # Get the text from the current page
                page = pdf_reader.pages[page_num]
                all_text += page.extract_text() 



    # Save the combined text to a single text file
    with open(output_text_file, 'w') as text_file:
        text_file.write(all_text)


# Call the function to merge PDFs and save as a text file
merge_pdfs_to_text(pdf_directory, 'combined_text.txt')

pdftext=''
# Load the content of the combined_text.txt file into the pdftext variable
with open('combined_text.txt', 'r') as file:
    pdftext = file.read()

# Prompt the user to enter the topic
topic = input("Please enter the topic for the literature review: ")


#this section is the prompt for the anthropic api
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.environ['ANTHROPIC_API_KEY'],
)

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1000,
    temperature=0,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You will be conducting a literature review on the following topic:\n\n<topic>\n"
                    + topic
                    + "\n</topic>\n\nTo assist you, I have provided a set of relevant papers and articles:\n\n<pdftext>\n"
                    + pdftext
                    + "\n</papers>\n\nPlease carefully read through each of these papers. As you read, take notes on the key themes, findings, debates, and research gaps across the different works. Your literature review should ONLY be based on the information contained in these provided papers. Do not include any additional information or examples beyond what is present in these papers.\n\nOnce you have read through everything, I would like you to write a literature review that synthesizes the main ideas and insights from this collection of papers. Your review should include the following sections:\n\n1. Introduction \n- Introduce the overall topic\n- Explain why this is an important area of research\n- Preview the key themes you will discuss\n\n2. Key Themes and Debates\n- Identify 3-5 major themes, findings, or debates that emerge from the papers\n- Within each theme, discuss how different authors approach the issue\n- Note any points of agreement or disagreement between papers\n- Cite the relevant papers when discussing their content\n\n3. Research Gaps and Future Directions \n- Highlight any gaps in the existing research that the papers reveal\n- Suggest some potential directions for future research on this topic\n\n4. Conclusion\n- Briefly summarize the key takeaways from your literature review\n- Reiterate the significance of this research area\n\nPlease write your completed literature review inside <literature-review> tags. Make sure to proofread your work for clarity and coherence before submitting.",
                }
            ],
        }
    ],
)
print(message.content)



   
