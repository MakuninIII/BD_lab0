import psycopg2
from prettytable import PrettyTable

def is_valid_title(title):
    return bool(title.strip())

def is_valid_id(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM path_enum WHERE id = %s", (node_id,))
        return cur.fetchone()[0] > 0

def print_tree(conn, node_id, level=0, visited=None):
    if visited is None:
        visited = set()

    with conn.cursor() as cur:
        try:
            cur.execute("SELECT id, title, path FROM path_enum WHERE id = %s", (node_id,))
            node = cur.fetchone()
            if not node:
                print("Node not found.")
                return

            if node_id in visited:
                return
            visited.add(node_id)

            if level == 0:
                print('-------------------------------------------')
                print(f"{node[1]} (ID: {node[0]})")
            else:
                print("|   " * (level - 1) + f"└── {node[1]} (ID: {node[0]})")

            cur.execute("""
                SELECT id, title 
                FROM path_enum 
                WHERE path = %s || id || '/'
                ORDER BY id
            """, (node[2],))
            children = cur.fetchall()

            for child in children:
                print_tree(conn, child[0], level + 1, visited)
        except psycopg2.Error as e:
            print("Error printing tree:", e)

# 1. Добавление листа
def add_leaf(conn, title, parent_id):
    if not is_valid_title(title):
        print("Error: Title cannot be empty or consist only of spaces.")
        return

    with conn.cursor() as cur:
        try:
            cur.execute("SELECT path FROM path_enum WHERE id = %s", (parent_id,))
            parent_path = cur.fetchone()
            if parent_path is None:
                raise ValueError(f"Parent ID {parent_id} does not exist.")
            
            cur.execute(
                "INSERT INTO path_enum (title, path) VALUES (%s, %s) RETURNING id",
                (title, parent_path[0])
            )
            new_id = cur.fetchone()[0]
            
            new_path = f"{parent_path[0]}{new_id}/"
            cur.execute(
                "UPDATE path_enum SET path = %s WHERE id = %s",
                (new_path, new_id)
            )
            
            conn.commit()
            return new_id
        except psycopg2.Error as e:
            print("Error adding leaf:", e)
            conn.rollback()
        except ValueError as ve:
            print(ve)
            conn.rollback()

# 2. Удаление листа
def delete_leaf(conn, node_id):
    if not is_valid_id(conn, node_id):
        print(f"Error: Node ID {node_id} does not exist.")
        return

    with conn.cursor() as cur:
        try:
            cur.execute("SELECT COUNT(*) FROM path_enum WHERE path LIKE %s AND id != %s", (f"%/{node_id}/%", node_id))
            if cur.fetchone()[0] > 0:
                print("Error: Node is not a leaf and cannot be deleted.")
                return False
            
            cur.execute("DELETE FROM path_enum WHERE id = %s", (node_id,))
            conn.commit()
            print(f"Leaf deleted successfully.")
            return True
        except psycopg2.Error as e:
            print("Error deleting leaf:", e)
            conn.rollback()

# 3. Удаление поддерева
def delete_subtree(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT path FROM path_enum WHERE id = %s", (node_id,))
            row = cur.fetchone()
            
            if not row:
                print(f"Node with ID {node_id} does not exist.")
                return
            
            cur.execute("SELECT id FROM path_enum WHERE path LIKE %s", (f"%/{node_id}/%",))
            result_ = cur.fetchone()
            if not result_:
                print(f"Error: Node ID {node_id} is root! You can't delete the entire tree.")
                return
            else:
                path = row[0]            
                cur.execute("""
                    DELETE FROM path_enum
                    WHERE path LIKE %s
                """, (f"{path}%",))
                
                conn.commit()
                print(f"Subtree with root ID {node_id} deleted successfully.")
        except psycopg2.Error as e:
            print("Error deleting subtree:", e)
            conn.rollback()

# 4. Удаление узла без поддерева
def delete_node_without_subtree(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT path FROM path_enum WHERE id = %s", (node_id,))
            result = cur.fetchone()
            if not result:
                print("Node not found.")
                return
            node_path = result[0]

            cur.execute("SELECT id FROM path_enum WHERE path LIKE %s", (f"%/{node_id}/%",))
            result_ = cur.fetchone()
            if not result_:
                print(f"Error: Node ID {node_id} is root, so the subtree cannot be reassigned.")
                return
            else:
                cur.execute("""
                    UPDATE path_enum 
                    SET path = REGEXP_REPLACE(path, '^' || %s, %s)
                    WHERE path LIKE %s || '%%' AND id != %s
                """, (node_path, node_path.rsplit("/", 2)[0] + "/", f"{node_path}", node_id))
                
                cur.execute("DELETE FROM path_enum WHERE id = %s", (node_id,))
                conn.commit()
                print(f"Node {node_id} deleted successfully without its subtree.")
        except psycopg2.Error as e:
            print("Error deleting node without subtree:", e)
            conn.rollback()

# 5. Получение прямых потомков
def get_direct_descendants(conn, node_id):
    if not is_valid_id(conn, node_id):
        print(f"Error: Node ID {node_id} does not exist.")
        return
            
    with conn.cursor() as cur:
        try:
            cur.execute("""
                    SELECT * 
                    FROM path_enum
                    WHERE SUBSTRING(
                        path, 
                        1, 
                        LENGTH(path) - POSITION('/' IN REVERSE(SUBSTRING(path, 1, LENGTH(path)-1)))
                    ) LIKE (SELECT path FROM path_enum WHERE id = %s) AND id != %s;
                """ , (f"{node_id}", node_id))
            result = cur.fetchall()
            if result:
                table = PrettyTable(["ID", "Title", "Path"])
                for row in result:
                    table.add_row(row)
                print(table)
            else:
                print("No direct descendants found.")
        except psycopg2.Error as e:
            print("Error retrieving direct descendants:", e)
            return None

# 6. Получение прямого родителя
def get_direct_parent(conn, node_id):
    if not is_valid_id(conn, node_id):
        print(f"Error: Node ID {node_id} does not exist.")
        return
    if node_id == 1:
        print(f"Node ID 1 is root and does not have a parent.")
        return
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT path FROM path_enum WHERE id = %s", (node_id,))
            result = cur.fetchone()
            if not result:
                return None

            parent_path = result[0].rsplit("/", 2)[0] + "/"
            cur.execute("SELECT id,title,path FROM path_enum WHERE path = %s", (parent_path,))
            result = cur.fetchone()
            if result:
                table = PrettyTable(["ID", "Title", "Path"])
                table.add_row(result)
                print(table)
            else:
                print("No parent found.")
        except psycopg2.Error as e:
            print("Error retrieving direct parent:", e)
            return None

# 7. Получение всех потомков
def get_all_descendants(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                    SELECT * 
                    FROM path_enum
                    WHERE SUBSTRING(
                        path, 
                        1, 
                        LENGTH(path) - POSITION('/' IN REVERSE(SUBSTRING(path, 1, LENGTH(path)-1)))
                    ) LIKE (SELECT path FROM path_enum WHERE id = %s) AND id != %s;
                """ , (f"{node_id}", node_id))
            result = cur.fetchall()
            if result:
                print_tree(conn, node_id)
            else:
                print("No descendants found.")
        except psycopg2.Error as e:
            print("Error retrieving direct parent:", e)
            return None

#8. Получение всех родителей
def get_all_parents(conn, node_id):
    if node_id == 1:
        print(f"Node ID 1 is root and does not have a parent.")
        return
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT path FROM path_enum WHERE id = %s", (node_id,))
            result = cur.fetchone()
            if not result:
                print("Node not found.")
                return

            node_path = result[0]
            path_parts = node_path.strip("/").split("/")

            if not path_parts:
                print("No parents found.")
                return

            parents = []
            for part in path_parts:
                cur.execute("SELECT id, title, path FROM path_enum WHERE id = %s", (part,))
                parents.append(cur.fetchone())

            for i, parent in enumerate(parents):
                is_last = (i == len(parents) - 1)
                prefix = "|   " if i < len(parents) - 1 else "    "
                if i == 0:
                    print(f"{parent[1]} (ID: {parent[0]})")
                else:
                    print(f"{' ' * (i * 4)}└── {parent[1]} (ID: {parent[0]})")
        except psycopg2.Error as e:
            print("Error retrieving all parents:", e)

    
# main
if __name__ == "__main__":
    try:
        with psycopg2.connect(
            dbname="Enum_path",
            user="postgres",
            password=" ",
            host="localhost"
        ) as conn:
            
            print_tree(conn, 1);
                
            while True:
                print("\n1. Add Leaf")
                print("2. Delete Leaf")
                print("3. Delete Subtree")
                print("4. Delete Node without Subtree")
                print("5. Get Direct Descendants")
                print("6. Get Direct Parent")
                print("7. Get All Descendants")
                print("8. Get All Parents")
                print("9. Print Tree")
                print("10. Exit")
                
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    title = input("Enter title of the new leaf: ")
                    parent_id = input("Enter parent ID: ")
                    try:
                        new_id = add_leaf(conn, title, int(parent_id))
                    except ValueError:
                        print("Invalid parent ID. Please enter a valid number.")

                elif choice == '2':
                    node_id = input("Enter leaf ID to delete: ")
                    try:
                        delete_leaf(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")
                
                elif choice == '3':
                    node_id = input("Enter node ID to delete subtree: ")
                    try:
                        delete_subtree(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")
                
                elif choice == '4':
                    node_id = input("Enter node ID to delete without subtree: ")
                    try:
                        delete_node_without_subtree(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")
                
                elif choice == '5':
                    node_id = input("Enter node ID to get direct descendants: ")
                    try:
                        get_direct_descendants(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")
                
                elif choice == '6':
                    node_id = input("Enter node ID to get direct parent: ")
                    try:
                        parent_id = get_direct_parent(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")
                
                elif choice == '7':
                    node_id = input("Enter node ID to get all descendants: ")
                    try:
                        descendants = get_all_descendants(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")
                
                elif choice == '8':
                    node_id = input("Enter node ID to get all parents: ")
                    try:
                        ancestors = get_all_parents(conn, int(node_id))
                    except ValueError:
                        print("Invalid node ID. Please enter a valid number.")

                elif choice == '9':
                    print_tree(conn, 1)

                elif choice == '10':
                    break
                
                else:
                    print("Invalid choice. Please try again.")
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
