import json
from xml.dom import minidom



def read_txt_from_local(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def parse_movies_string(movies_str: str) -> list:
    movie_list = []
    movie_info = movies_str.strip().split("\n\n")

      # Remove header

    for movie in movie_info:
        parts = movie.split("\n")
        d = []
        for part in parts:
            parts = part.split(":")
            if parts[0].strip() == "Director Name":
                for part in parts[1].strip().split(","):
                    d.append({"Director": {"Name": part.strip()}})
            else:
                d.append({parts[0].strip(): parts[1].strip(" ")})
        movie_list.append({"Movie": d})
    return movie_list


def sort_movies_by_title(movie_list: list) -> list:
    return sorted(movie_list, key=lambda m: m["Movie"][0]["Title"])


def convert_movies_to_xml(movie_list: list) -> minidom.Document:
    doc = minidom.Document()
    movies_element = doc.createElement("Movies")
    doc.appendChild(movies_element)

    for movie in movie_list:
        movie_element = doc.createElement("Movie")
        for m in movie["Movie"]:
            for key, value in m.items():
                if key == "Director":
                    director_element = doc.createElement("Director")
                    for name in value["Name"]:
                        name_element = doc.createElement("Name")
                        name_element.appendChild(doc.createTextNode(name))
                        director_element.appendChild(name_element)
                    movie_element.appendChild(director_element)
                else:
                    element = doc.createElement(key)
                    element.appendChild(doc.createTextNode(value))
                    movie_element.appendChild(element)
            movies_element.appendChild(movie_element)

    return doc


def main():
    # Read movie data
    with open("./movies.txt", "r", encoding="utf-8") as file:
        content = file.read()
        movie_list = parse_movies_string(content)

    # Output unsorted JSON
    with open("movies_not_sorted.json", "w", encoding="utf-8") as f:
        json.dump({"Movies": movie_list}, f, indent=4)

    # Sort and output sorted JSON
    sorted_movies = sort_movies_by_title(movie_list)
    with open("MoviesSorted.json", "w", encoding="utf-8") as f:
        json.dump({"Movies": sorted_movies}, f, indent=4)

    # Convert sorted movies to XML
    xml_doc = convert_movies_to_xml(sorted_movies)
    with open("Movies.xml", "w", encoding="utf-8") as f:
        f.write(xml_doc.toprettyxml(indent="  "))


if __name__ == "__main__":
    main()
