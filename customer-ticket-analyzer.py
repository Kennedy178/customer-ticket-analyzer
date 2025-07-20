import string
from collections import Counter
import csv

# Input Handling
def getUserMessage():
    while True:
        try:
            message = input("Enter your message (or 'quit' to exit): ").strip()
            if not message:
                raise ValueError("Message cannot be empty!")

            if message.isdigit():
                print("Warning: Message contains only numbers. Did you mean to text?")

            return message

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")

# LowercaseFilter Class - Cleans text
class LowercaseFilter:
    def __init__(self, message):
        # Clean the message in __init__
        self.cleaned_message = message
        for char in string.punctuation:
            self.cleaned_message = self.cleaned_message.replace(char, '')
        self.cleaned_message = self.cleaned_message.lower()

    def get_cleaned_message(self):
        return self.cleaned_message

# ClassifyMessage Class - Classifies & Counts Frequencies
class ClassifyMessage:
    CATEGORIES = {
        "Complaint": ["error", "failed", "problem"],
        "Request": ["please", "help", "support"],
        "Feedback": ["thanks", "great", "awesome"]
    }

    def __init__(self, message):
        self.message = message

    def classify_message(self):
        for category, keywords in self.CATEGORIES.items():
            if any(keyword in self.message for keyword in keywords):
                return category
        return "General Inquiry"

    def freq_all(self):
        word_list = self.message.split()
        freq_dict = {}
        for word in word_list:
            freq_dict[word] = freq_dict.get(word, 0) + 1
        return freq_dict

    def freq_of(self, word):
        return self.freq_all().get(word.lower(), 0)

    @staticmethod
    def display_summary_statistics(classified_list):
        stats = Counter(classified_list)
        total = len(classified_list)
        print("\n📊 Summary Statistics:")
        print("-------------------")
        print(f"Total Messages: {total}")
        for category, count in stats.items():
            percent = (count / total) * 100 if total > 0 else 0
            print(f"- {category}: {count} ({percent:.1f}%)")

# Main Program Flow
def main():
    all_classifications = []
    all_messages = []

    while True:
        message = getUserMessage()
        if message.lower() in ["quit", "exit"]:
            break

        # Clean message
        cleaner = LowercaseFilter(message)
        cleaned_message = cleaner.get_cleaned_message()

        # Classify message
        classifier = ClassifyMessage(cleaned_message)
        category = classifier.classify_message()

        # Collect results
        all_classifications.append(category)
        all_messages.append((message, cleaned_message, category))

        # Show user immediate feedback
        print(f"\nOriginal: {message}")
        print(f"Cleaned: {cleaned_message}")
        print(f"Category: {category}")
        print(f"Word Frequencies: {classifier.freq_all()}")
        print("-" * 30)

    # Summary stats
    ClassifyMessage.display_summary_statistics(all_classifications)

    # Save to CSV
    with open("classified_messages.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Message", "Cleaned Message", "Category"])
        writer.writerows(all_messages)

    print("\nMessages saved to 'classified_messages.csv'. Goodbye!")

# Run the Program
if __name__ == "__main__":
    main()
