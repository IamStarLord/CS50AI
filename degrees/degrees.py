import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    # This fucntion opens the people.csv file then proceedes to add 
    # the name, birth and set of movies the  person has been in (initally set to empty set)
    # furthermore it adds the names to the names dictionary which maps name to id 
    # How does it handle the duplicate names situation ?
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    # this function populates the movies dictionary with 
    # the mapping being id to title, year and stars
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    # the stars.csv file maps person id to the movie id
    # this function adds the movies to the dictionary with the person_id 
    # it also adds the person_id(s) with the movie_id
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError: # raised when you access a key  that isn't in the dictionary 
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]") # Make sure only two arguments given to the command line 
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"  # default dictionary is large if none is provied

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: ")) # Stores persons id corresponding to their name 
    if source is None:
        sys.exit("Person not found.") # throw an error to the command line 
    target = person_id_for_name(input("Name: ")) # Id of the "goal" person
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target) # find the shortest path between the two people

    if path is None: # path is an abbrevieated list of names I suppose 
        print("Not connected.") 
    else:
        degrees = len(path) # degrees is equal to the length of the path 
        print(f"{degrees} degrees of separation.")
        print(path)
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    # psuedocode 
    # get all the neighbours of the source 
    # for each tuple 
    # make a node of it
    # add neighbours to the queueFrontier
    # for each node in neighbours 
    # if 

    # number of explored states
    num_explored = 0

    # initialize frontier to the source 
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set() # Initially its initaialized to an empty set

    path = list()

    # loop until source is found 
    while True:

        # return None if frontier is empty
        if frontier.empty(): 
            return None 

        # Choose a node from the frontier 
        node = frontier.remove()
        num_explored += 1

        # check if node is the goal 
        if node.state == target:
            # backtract your way to source 
            while node.parent is not None:
                # append parent to node
                path.append((node.action, node.state))
                node = node.parent 
            path.reverse() 
            return path
        
        # Mark node's state as explored 
        explored.add(node.state)

        # Add neightbours to the frontier 
        # action and state correspond to movie_id and person_id
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set())) # convert the dictionary to a list with the name providedonly 
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"] # all the movies of person with person_id
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]: # get the stars of each of those movies 
            neighbors.add((movie_id, person_id)) # Add that movie id and person id 
    return neighbors


if __name__ == "__main__":
    main()
