import psycopg2
from prettytable import PrettyTable

def print_tree(conn, node_id, level=0):
    with conn.cursor() as cur:
        cur.execute("SELECT title FROM neighbor_tree WHERE id = %s", (node_id,))
        node = cur.fetchone()
        if node is None:
            return
        
        print(" " * (level * 4) + f"└── {node[0]}")

        cur.execute("SELECT id FROM neighbor_tree WHERE parent_id = %s", (node_id,))
        children = cur.fetchall()
        
        for child in children:
            print_tree(conn, child[0], level + 1)

# 1. Добавление листа
def add_leaf(conn, title, parent_id):
    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO neighbor_tree (title, parent_id) VALUES (%s, %s) RETURNING id",
                (title, parent_id)
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id
        except psycopg2.Error as e:
            print("Error adding leaf:", e)
            conn.rollback()
            return None

# 2. Удаление листа
def delete_leaf(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT COUNT(*) FROM neighbor_tree WHERE parent_id = %s", (node_id,))
            if cur.fetchone()[0] > 0:
                print("Узел не является листом и не может быть удален.")
                return None
            cur.execute("DELETE FROM neighbor_tree WHERE id = %s RETURNING id", (node_id,))
            deleted_id = cur.fetchone()
            conn.commit()
            return deleted_id[0] if deleted_id else None
        except psycopg2.Error as e:
            print("Error deleting leaf:", e)
            conn.rollback()
            return None

# 3. Удаление поддерева
def delete_subtree(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("WITH RECURSIVE sub_tree AS ( \
                            SELECT id FROM neighbor_tree WHERE id = %s \
                            UNION ALL \
                            SELECT nt.id FROM neighbor_tree nt \
                            JOIN sub_tree st ON nt.parent_id = st.id \
                         ) DELETE FROM neighbor_tree WHERE id IN (SELECT id FROM sub_tree) RETURNING id",
                         (node_id,))
            deleted_ids = [row[0] for row in cur.fetchall()]
            conn.commit()
            return deleted_ids
        except psycopg2.Error as e:
            print("Error deleting subtree:", e)
            conn.rollback()
            return None

# 4. Удаление узла без поддерева
def delete_node_without_subtree(conn, node_id):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT parent_id FROM neighbor_tree WHERE id = %s", (node_id,))
            result = cur.fetchone()
            if not result:
                print("Node not found.")
                return None
            parent_id = result[0]

            cur.execute("UPDATE neighbor_tree SET parent_id = %s WHERE parent_id = %s", (parent_id, node_id))
            cur.execute("DELETE FROM neighbor_tree WHERE id = %s RETURNING id", (node_id,))
            deleted_id = cur.fetchone()
            conn.commit()
            return deleted_id[0] if deleted_id else None
        except psycopg2.Error as e:
            print("Error deleting node without subtree:", e)
            conn.rollback()
            return None

# 5. Получение прямых потомков
def get_direct_descendants(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, parent_id FROM neighbor_tree WHERE parent_id = %s", (node_id,))
        return cur.fetchall()

# 6. Получение прямого родителя
def get_direct_parent(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, parent_id FROM neighbor_tree WHERE id = %s", (node_id,))
        return cur.fetchone()

# 7. Получение всех потомков
def get_all_descendants(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("WITH RECURSIVE descendants AS ( \
                        SELECT id, title FROM neighbor_tree WHERE parent_id = %s \
                        UNION ALL \
                        SELECT nt.id, nt.title FROM neighbor_tree nt \
                        JOIN descendants d ON nt.parent_id = d.id \
                     ) SELECT * FROM descendants", 
                     (node_id,))
        descendants = cur.fetchall()
        return build_tree_from_list(descendants, node_id)

# 8. Получение всех родителей
def get_all_ancestors(conn, node_id):
    with conn.cursor() as cur:
        cur.execute("WITH RECURSIVE ancestors AS ( \
                        SELECT id, parent_id, title FROM neighbor_tree WHERE id = %s \
                        UNION ALL \
                        SELECT nt.id, nt.parent_id, nt.title FROM neighbor_tree nt \
                        JOIN ancestors a ON nt.id = a.parent_id \
                     ) SELECT id, title FROM ancestors WHERE id != %s", 
                     (node_id, node_id))
        ancestors = cur.fetchall()
        return build_tree_from_list(ancestors[::-1], node_id)

# Построение дерева из списка узлов
def build_tree_from_list(nodes, root_id, level=0):
    tree = ""
    for node in nodes:
        tree += " " * (level * 4) + f"└── {node[1]}\n"
        level += 1
    return tree

 # result = cur.fetchall()
        
        # if not result:
        #     print("No descendants tree found for the given node ID.")
        #     return
        
        # for row in result:
        #     level_1_id, level_1_title, level_2_id, level_2_title, level_3_id, level_3_title, level_4_id, level_4_title, level_5_id, level_5_title = row
            
        #     print(f"{level_1_title} (ID: {level_1_id})")

        #     if level_2_id is not None:
        #         print(f"    └── {level_2_title} (ID: {level_2_id})")
        #     if level_3_id is not None:
        #         print(f"        └── {level_3_title} (ID: {level_3_id})")
        #     if level_4_id is not None:
        #         print(f"            └── {level_4_title} (ID: {level_4_id})")
        #     if level_5_id is not None:
        #         print(f"                {level_5_title} (ID: {level_5_id})")




        # import psycopg2
# from prettytable import PrettyTable

# def is_valid_title(title):
#     """Проверяет, является ли название валидным (не пустым и не состоящим только из пробелов)."""
#     return bool(title.strip())

# def is_valid_id(conn, node_id):
#     """Проверяет, существует ли узел с данным ID."""
#     with conn.cursor() as cur:
#         cur.execute("SELECT COUNT(*) FROM neighbor_tree WHERE id = %s", (node_id,))
#         return cur.fetchone()[0] > 0
    
# def print_tree(conn, node_id, level=0):
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, title FROM neighbor_tree WHERE id = %s", (node_id,))
#         node = cur.fetchone()
#         if node is None:
#             print("No descendants tree found for the given node ID.")
#             return
        
#         if level == 0:
#             print(f"{node[1]} (ID: {node[0]})")
#         else:
#             print(" " * (level * 4) + f"└── {node[1]} (ID: {node[0]})")

#         cur.execute("SELECT id FROM neighbor_tree WHERE parent_id = %s", (node_id,))
#         children = cur.fetchall()
        
#         for child in children:
#             print_tree(conn, child[0], level + 1)

# # 1. Добавление листа
# def add_leaf(conn, title, parent_id):
#     with conn.cursor() as cur:
#         try:
#             cur.execute(
#                 "INSERT INTO neighbor_tree (title, parent_id) VALUES (%s, %s) RETURNING id",
#                 (title, parent_id)
#             )
#             new_id = cur.fetchone()[0]
#             conn.commit()
#             return new_id
#         except psycopg2.Error as e:
#             print("Error adding leaf:", e)
#             conn.rollback()

# # 2. Удаление листа
# def delete_leaf(conn, node_id):
#     with conn.cursor() as cur:
#         try:
#             cur.execute("SELECT COUNT(*) FROM neighbor_tree WHERE parent_id = %s", (node_id,))
#             if cur.fetchone()[0] > 0:
#                 print("Узел не является листом и не может быть удален.")
#                 return False
#             cur.execute("DELETE FROM neighbor_tree WHERE id = %s", (node_id,))
#             conn.commit()
#             return True
#         except psycopg2.Error as e:
#             print("Error deleting leaf:", e)
#             conn.rollback()

# # 3. Удаление поддерева
# def delete_subtree(conn, node_id):
#     with conn.cursor() as cur:
#         try:
#             cur.execute("WITH RECURSIVE sub_tree AS ( \
#                             SELECT id FROM neighbor_tree WHERE id = %s \
#                             UNION ALL \
#                             SELECT nt.id FROM neighbor_tree nt \
#                             JOIN sub_tree st ON nt.parent_id = st.id \
#                          ) DELETE FROM neighbor_tree WHERE id IN (SELECT id FROM sub_tree)",
#                          (node_id,))
#             conn.commit()
#         except psycopg2.Error as e:
#             print("Error deleting subtree:", e)
#             conn.rollback()

# # 4. Удаление узла без поддерева
# def delete_node_without_subtree(conn, node_id):
#     with conn.cursor() as cur:
#         try:
#             cur.execute("SELECT parent_id FROM neighbor_tree WHERE id = %s", (node_id,))
#             result = cur.fetchone()
#             if not result:
#                 print("Node not found.")
#                 return
#             parent_id = result[0]

#             cur.execute("UPDATE neighbor_tree SET parent_id = %s WHERE parent_id = %s", (parent_id, node_id))
#             cur.execute("DELETE FROM neighbor_tree WHERE id = %s", (node_id,))
#             conn.commit()
#         except psycopg2.Error as e:
#             print("Error deleting node without subtree:", e)
#             conn.rollback()

# # 5. Получение прямых потомков
# def get_direct_descendants(conn, node_id):
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM neighbor_tree WHERE parent_id = %s", (node_id,))
#         result = cur.fetchall()
#         return result if result else None

# # 6. Получение прямого родителя
# def get_direct_parent(conn, node_id):
#     with conn.cursor() as cur:
#         cur.execute("SELECT id, title, parent_id FROM neighbor_tree WHERE id = %s", (node_id,))
#         result = cur.fetchone()
#         return result[0] if result else None

# # 7. Получение всех потомков
# def get_all_descendants(conn, node_id):
#     with conn.cursor() as cur:
#         cur.execute(""" 
#             SELECT h1.id AS level_1_id, h1.title AS level_1_title,
#                    h2.id AS level_2_id, h2.title AS level_2_title,
#                    h3.id AS level_3_id, h3.title AS level_3_title,
#                    h4.id AS level_4_id, h4.title AS level_4_title,
#                    h5.id AS level_5_id, h5.title AS level_5_title
#             FROM neighbor_tree AS h1
#             LEFT JOIN neighbor_tree AS h2 ON h2.parent_id = h1.id
#             LEFT JOIN neighbor_tree AS h3 ON h3.parent_id = h2.id
#             LEFT JOIN neighbor_tree AS h4 ON h4.parent_id = h3.id
#             LEFT JOIN neighbor_tree AS h5 ON h5.parent_id = h4.id  
#             WHERE h1.id = %s
#         """, (node_id,))
        
#         print_tree(conn, node_id, level=0)
       
    
# # 8. Получение всех родителей
# def get_all_parents(conn, node_id):
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT h1.id AS level_1_id, h1.title AS level_1_title,
#                     h2.id AS level_2_id, h2.title AS level_2_title,
#                     h3.id AS level_3_id, h3.title AS level_3_title,
#                     h4.id AS level_4_id, h4.title AS level_4_title,
#                     h5.id AS level_5_id, h5.title AS level_5_title 
#             FROM neighbor_tree AS h1
#             LEFT JOIN neighbor_tree AS h2 ON h1.parent_id = h2.id
#             LEFT JOIN neighbor_tree AS h3 ON h2.parent_id = h3.id
#             LEFT JOIN neighbor_tree AS h4 ON h3.parent_id = h4.id
#             LEFT JOIN neighbor_tree AS h5 ON h4.parent_id = h5.id
#             WHERE h1.id = %s
#         """, (node_id,))

#         result = cur.fetchall()
        
#         if not result:
#             print("No parent tree found for the given node ID.")
#             return
        
#         for row in result:
#             level_1_id, level_1_title, level_2_id, level_2_title, level_3_id, level_3_title, level_4_id, level_4_title, level_5_id, level_5_title = row
            
#             if level_5_id is not None:
#                 print(f"{level_5_title} (ID: {level_5_id})")
#             if level_4_id is not None:
#                 if level_4_id == 1:
#                     print(f"{level_4_title} (ID: {level_4_id})")
#                 else:
#                     print(f"    └── {level_4_title} (ID: {level_4_id})")  
#             if level_3_id is not None:
#                 if level_3_id == 1:
#                     print(f"{level_3_title} (ID: {level_3_id})")
#                 else:
#                     print(f"        └── {level_3_title} (ID: {level_3_id})")
#             if level_2_id is not None:
#                 if level_2_id == 1:
#                     print(f"{level_2_title} (ID: {level_2_id})")
#                 else:
#                     print(f"            └── {level_2_title} (ID: {level_2_id})")
#             print(f"                └── {level_1_title} (ID: {level_1_id})")

    
# # main
# if __name__ == "__main__":
#     try:
#         with psycopg2.connect(
#             dbname="Neighbor_tree",
#             user="postgres",
#             password=" ",
#             host="localhost"
#         ) as conn:
            
#             print_tree(conn, 1);

#             while True:
#                 print("\n1. Add Leaf")
#                 print("2. Delete Leaf")
#                 print("3. Delete Subtree")
#                 print("4. Delete Node without Subtree")
#                 print("5. Get Direct Descendants")
#                 print("6. Get Direct Parent")
#                 print("7. Get All Descendants")
#                 print("8. Get All Parents")
#                 print("9. Exit")
                
#                 choice = input("Enter your choice: ")
                
#                 if choice == '1':
#                     title = input("Enter title of the new leaf: ")
#                     parent_id = input("Enter parent ID: ")
#                     try:
#                         new_id = add_leaf(conn, title, int(parent_id))
#                         print(f"Leaf added with ID: {new_id}")
#                     except ValueError:
#                         print("Invalid parent ID. Please enter a valid number.")

#                 elif choice == '2':
#                     node_id = input("Enter leaf ID to delete: ")
#                     try:
#                         if delete_leaf(conn, int(node_id)):
#                             print("Leaf deleted successfully.")
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")
                
#                 elif choice == '3':
#                     node_id = input("Enter node ID to delete subtree: ")
#                     try:
#                         delete_subtree(conn, int(node_id))
#                         print("Subtree deleted successfully.")
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")
                
#                 elif choice == '4':
#                     node_id = input("Enter node ID to delete without subtree: ")
#                     try:
#                         delete_node_without_subtree(conn, int(node_id))
#                         print("Node deleted without subtree.")
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")
                
#                 elif choice == '5':
#                     node_id = input("Enter node ID to get direct descendants: ")
#                     try:
#                         descendants = get_direct_descendants(conn, int(node_id))
#                         if descendants is not None:
#                             table = PrettyTable(["ID", "Title", "Parent_id"])
#                             for d in descendants:
#                                 table.add_row(d)
#                             print(table)
#                         else:
#                             print("No descedants found.")
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")
                
#                 elif choice == '6':
#                     node_id = input("Enter node ID to get direct parent: ")
#                     try:
#                         parent_id = get_direct_parent(conn, int(node_id))
#                         if parent_id is not None:
#                             print(f"Direct parent ID: {parent_id}")
#                         else:
#                             print("No parent found.")
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")
                
#                 elif choice == '7':
#                     node_id = input("Enter node ID to get all descendants: ")
#                     try:
#                         print('-------------------------------------------')
#                         descendants = get_all_descendants(conn, int(node_id))
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")
                
#                 elif choice == '8':
#                     node_id = input("Enter node ID to get all parents: ")
#                     try:
#                         print('-------------------------------------------')
#                         ancestors = get_all_parents(conn, int(node_id))
#                     except ValueError:
#                         print("Invalid node ID. Please enter a valid number.")

#                 elif choice == '9':
#                     break
                
#                 else:
#                     print("Invalid choice. Please try again.")
#     except psycopg2.Error as e:
#         print("Error connecting to the database:", e)

