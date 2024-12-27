import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

def get_wikipedia_content(page_name):
    try:
        # Try to get the page directly
        page = wikipedia.page(page_name, auto_suggest=False)
        return page.summary
        
    except DisambiguationError as e:
        # Handle disambiguation pages
        result_string = f"'{page_name}' could refer to multiple articles. Try one of these:\n"
        for option in e.options[:10]:  # Limit to first 10 options
            result_string += f"• {option}\n"
        return result_string
        
    except PageError:
        # Handle pages that don't exist by searching
        search_results = wikipedia.search(page_name, results=10)
        if not search_results:
            return f"No Wikipedia articles found for '{page_name}'"
            
        result_string = f"I didn't find a perfect match for '{page_name}', but you can try one of these:\n"
        for result in search_results:
            result_string += f"• {result}\n"
        return result_string