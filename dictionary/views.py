def index():
    """
    Returns an index page if request is GET
    Redirects to search views if request is POST
    """
    pass


def manual():
    """
    Returns a static how-to-use page
    """
    pass


def about():
    """
    Returns a static about page
    """
    pass


def bibliography():
    """
    Returns a static bibliography page
    """
    pass


def simple_search():
    """
    Performs search in dominants given an input string
    Returns the result page
    """
    pass

# note: in current implementation, the difference between exact query and extended query over dominants
# is that extended query allows substring matching
# todo do we want to recreate this ^ behavior?


def extended_search():
    """
    Reads the search parameters and performs search in relevant places
    Parameters may be several (e.g. dominant and row)
    """
    # todo maybe split different modes into different views or functions, not sure yet
    pass

# todo extended search should have an explicit substring checkbox somewhere in the template