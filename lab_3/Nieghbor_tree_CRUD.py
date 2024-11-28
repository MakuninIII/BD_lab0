import psycopg2
from prettytable import PrettyTable

def is_valid_title(title):
    return bool(title.strip())

def is_valid_id(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM neighbor_tree WHERE id = %s", (node_id,))
        return cur.fetchone()[0] > 0

def print_tree(conn, node_id, level=0):
    with conn.cursor() as cur:
        cur.execute("SELECT id, title FROM neighbor_tree WHERE id = %s", (node_id,))
        node = cur.fetchone()
        if node is None:
            print("Node not found.")
            return

        if level == 0:
            print('-------------------------------------------')
            print(f"{node[1]} (ID: {node[0]})")
        else:
            print(" " * (level * 4) + f"└── {node[1]} (ID: {node[0]})")

        cur.execute("SELECT id FROM neighbor_tree WHERE parent_id = %s", (node_id,))
        children = cur.fetchall()

        for child in children:
            print_tree(conn, child[0], level + 1)

# 1. Добавление листа
def add_leaf(conn, title, parent_id):
    if not is_valid_title(title):
        print("Error: Title cannot be empty or consist only of spaces.")
        return

    if not is_valid_id(conn, parent_id):
        print(f"Error: Parent ID {parent_id} does not exist.")
        return

    with conn.cursor() as cur:
        title = title.strip()
        try:
            cur.execute(
                "INSERT INTO neighbor_tree (title, parent_id) VALUES (%s, %s) RETURNING id",
                (title, parent_id)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"Leaf added successfully with ID: {new_id}")
            return new_id
        except psycopg2.Error as e:
            print("Error adding leaf:", e)
            conn.rollback()

# 2. Удаление листа
def delete_leaf(conn, node_id):
    if not is_valid_id(conn, node_id):
        print(f"Error: Node ID {node_id} does not exist.")
        return

    with conn.cursor() as cur:
        try:
            cur.execute("SELECT COUNT(*) FROM neighbor_tree WHERE parent_id = %s", (node_id,))
            if cur.fetchone()[0] > 0:
                print("Error: Node is not a leaf and cannot be deleted.")
                return
            cur.execute("DELETE FROM neighbor_tree WHERE id = %s", (node_id,))
            conn.commit()
            print("Leaf deleted successfully.")
        except psycopg2.Error as e:
            print("Error deleting leaf:", e)
            conn.rollback()

# 3. Удаление поддерева
def delete_subtree(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT 1 FROM neighbor_tree WHERE id = %s", (node_id,))
            if cur.fetchone() is None:
                print(f"Error: Node ID {node_id} does not exist.")
                return False 
            
            cur.execute("""
                WITH RECURSIVE sub_tree AS (
                    SELECT id FROM neighbor_tree WHERE id = %s
                    UNION ALL
                    SELECT nt.id FROM neighbor_tree nt
                    JOIN sub_tree st ON nt.parent_id = st.id
                )
                DELETE FROM neighbor_tree WHERE id IN (SELECT id FROM sub_tree)
            """, (node_id,))
            conn.commit()
            print(f"Subtree with root ID {node_id} deleted successfully.")
            return True
        except psycopg2.Error as e:
            print("Error deleting subtree:", e)
            conn.rollback()
            return False

# 4. Удаление узла без поддерева
def delete_node_without_subtree(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT parent_id FROM neighbor_tree WHERE id = %s", (node_id,))
            result = cur.fetchone()
            if not result:
                print(f"Error: Node ID {node_id} does not exist.")
                return

            parent_id = result[0]
            cur.execute("UPDATE neighbor_tree SET parent_id = %s WHERE parent_id = %s", (parent_id, node_id))
            cur.execute("DELETE FROM neighbor_tree WHERE id = %s", (node_id,))
            conn.commit()
            print(f"Node with ID {node_id} deleted without subtree.")
        except psycopg2.Error as e:
            print("Error deleting node without subtree:", e)
            conn.rollback()

# 5. Получение прямых потомков
def get_direct_descendants(conn, node_id):
    if not is_valid_id(conn, node_id):
        print(f"Error: Node ID {node_id} does not exist.")
        return

    with conn.cursor() as cur:
        cur.execute("SELECT id, title, parent_id FROM neighbor_tree WHERE parent_id = %s", (node_id,))
        result = cur.fetchall()
        if result:
            table = PrettyTable(["ID", "Title", "Parent ID"])
            for row in result:
                table.add_row(row)
            print(table)
        else:
            print("No direct descendants found.")

# 6. Получение прямого родителя
def get_direct_parent(conn, node_id):
    if not is_valid_id(conn, node_id):
        print(f"Error: Node ID {node_id} does not exist.")
        return

    with conn.cursor() as cur:
        cur.execute("SELECT parent_id FROM neighbor_tree WHERE id = %s", (node_id,))
        result = cur.fetchone()
        cur.execute("SELECT id, title, parent_id FROM neighbor_tree WHERE id = %s", (result,))
        result = cur.fetchone()
        if result:
            table = PrettyTable(["ID", "Title", "Parent ID"])
            table.add_row(result)
            print(table)
        else:
            print("No parent found.")

# 7. Получение всех потомков
def get_all_descendants(conn, node_id):
    with conn.cursor() as cur:
        cur.execute(""" 
            SELECT h1.id AS level_1_id, h1.title AS level_1_title,
                   h2.id AS level_2_id, h2.title AS level_2_title,
                   h3.id AS level_3_id, h3.title AS level_3_title,
                   h4.id AS level_4_id, h4.title AS level_4_title,
                   h5.id AS level_5_id, h5.title AS level_5_title
            FROM neighbor_tree AS h1
            LEFT JOIN neighbor_tree AS h2 ON h2.parent_id = h1.id
            LEFT JOIN neighbor_tree AS h3 ON h3.parent_id = h2.id
            LEFT JOIN neighbor_tree AS h4 ON h4.parent_id = h3.id
            LEFT JOIN neighbor_tree AS h5 ON h5.parent_id = h4.id  
            WHERE h1.id = %s
        """, (node_id,))
        
        print_tree(conn, node_id, level=0)
       
    
# 8. Получение всех родителей
def get_all_parents(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT h1.id AS level_1_id, h1.title AS level_1_title,
                    h2.id AS level_2_id, h2.title AS level_2_title,
                    h3.id AS level_3_id, h3.title AS level_3_title,
                    h4.id AS level_4_id, h4.title AS level_4_title,
                    h5.id AS level_5_id, h5.title AS level_5_title 
            FROM neighbor_tree AS h1
            LEFT JOIN neighbor_tree AS h2 ON h1.parent_id = h2.id
            LEFT JOIN neighbor_tree AS h3 ON h2.parent_id = h3.id
            LEFT JOIN neighbor_tree AS h4 ON h3.parent_id = h4.id
            LEFT JOIN neighbor_tree AS h5 ON h4.parent_id = h5.id
            WHERE h1.id = %s
        """, (node_id,))

        result = cur.fetchall()
        
        if not result:
            print("No parent tree found for the given node ID.")
            return
        
        for row in result:
            level_1_id, level_1_title, level_2_id, level_2_title, level_3_id, level_3_title, level_4_id, level_4_title, level_5_id, level_5_title = row
            
            print('-------------------------------------------')
            if level_5_id is not None:
                print(f"{level_5_title} (ID: {level_5_id})")
            if level_4_id is not None:
                if level_4_id == 1:
                    print(f"{level_4_title} (ID: {level_4_id})")
                else:
                    print(f"    └── {level_4_title} (ID: {level_4_id})")  
            if level_3_id is not None:
                if level_3_id == 1:
                    print(f"{level_3_title} (ID: {level_3_id})")
                else:
                    print(f"        └── {level_3_title} (ID: {level_3_id})")
            if level_2_id is not None:
                if level_2_id == 1:
                    print(f"{level_2_title} (ID: {level_2_id})")
                else:
                    print(f"            └── {level_2_title} (ID: {level_2_id})")
            print(f"                └── {level_1_title} (ID: {level_1_id})")


# Main
if __name__ == "__main__":
    try:
        with psycopg2.connect(
            dbname="Neighbor_tree",
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
                print("9. Exit")
                
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    title = input("Enter title of the new leaf: ")
                    parent_id = input("Enter parent ID: ")
                    try:
                        new_id = add_leaf(conn, title, int(parent_id))
                        print(f"Leaf added with ID: {new_id}")
                    except ValueError:
                        print("Invalid parent ID. Please enter a valid number.")

                elif choice == '2':
                    node_id = input("Enter leaf ID to delete: ")
                    try:
                        if delete_leaf(conn, int(node_id)):
                            print("Leaf deleted successfully.")
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
                        get_direct_parent(conn, int(node_id))
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
                    break
                
                else:
                    print("Invalid choice. Please try again.")
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)