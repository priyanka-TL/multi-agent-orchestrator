from langchain_core.tools import tool
from ddgs import DDGS

# The @tool decorator registers this function as a tool that the LLM can call
@tool
def youtube_search_tool(query: str) -> str:
    """
    Searches YouTube for videos related to the query and returns titles and links.
    Always use this tool if the user asks for a video, tutorial, or visual reference.
    Falls back to web search for tutorials if YouTube search is unavailable.
    """
    try:
        # DDGS().videos performs a DuckDuckGo YouTube search
        results = DDGS().videos(query, max_results=3)
        if not results:
            # No YouTube results, try fallback web search for tutorials
            return _fallback_to_tutorial_search(query)

        # Format the raw JSON results into a readable string for the LLM
        response = "Here are some relevant YouTube videos:\n"
        for idx, res in enumerate(results, 1):
            title = res.get('title', 'Unknown Title')
            link = res.get('content', '')
            if not link:
                link = res.get('url', 'No link available')
            response += f"{idx}. [{title}]({link})\n"
        return response
    except Exception:
        # YouTube search service unavailable, fall back to tutorial search
        return _fallback_to_tutorial_search(query)


def _fallback_to_tutorial_search(query: str) -> str:
    """
    Fallback search when YouTube is unavailable.
    Searches for tutorials on the web instead.
    """
    try:
        tutorial_query = f"{query} tutorial"
        results = DDGS().text(tutorial_query, max_results=3)

        if not results:
            return "I couldn't find video tutorials or web resources for that query. Please try a different search term."

        response = "YouTube search is currently unavailable. Here are some tutorial resources from the web instead:\n"
        for idx, res in enumerate(results, 1):
            title = res.get('title', 'Unknown Title')
            link = res.get('href', '')
            response += f"{idx}. [{title}]({link})\n"
        return response
    except Exception as e:
        return f"Unable to search for resources: {str(e)}"

@tool
def web_search_tool(query: str) -> str:
    """
    Searches the general web for information related to the query.
    Use this to find references, articles, and factual information.
    """
    try:
        # DDGS().text performs a standard web text search
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No search results found."
            
        # Format the results into Markdown
        response = "Here is what I found on the web:\n"
        for idx, res in enumerate(results, 1):
            title = res.get('title', 'Unknown Title')
            body = res.get('body', '')
            link = res.get('href', '')
            response += f"{idx}. **[{title}]({link})**\n   {body}\n"
        return response
    except Exception as e:
        return f"Error searching the web: {str(e)}"
