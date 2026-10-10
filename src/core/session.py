import json
import os

# Clase para gestionar la sesión del usuario y permisos por rol
class SessionManager:
    def __init__(self):
        # Almacena los datos de la sesión actual en memoria
        self.session_data = None
        # Ruta donde se guardará el archivo de sesión
        self.session_file = "storage/temp/session.json"
    
    def save_session(self, user_data: dict):
        """
        Guarda los datos del usuario en un archivo JSON
        
        Args:
            user_data (dict): Diccionario con los datos del usuario (sin contraseña)
                Debe contener al menos: 'role', 'user', 'name', 'ci', etc.
        """
        try:
            # Crear el directorio si no existe
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            
            # Guardar los datos en el archivo JSON
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
            
            # Actualizar también los datos en memoria
            self.session_data = user_data
            
        except Exception as e:
            print(f"Error al guardar sesión: {e}")
            raise
    
    def load_session(self) -> dict:
        """
        Carga los datos de sesión desde el archivo JSON
        
        Returns:
            dict: Diccionario con los datos del usuario, o None si no hay sesión
        """
        try:
            # Si ya tenemos los datos en memoria, los retornamos
            if self.session_data:
                return self.session_data
            
            # Si el archivo existe, lo leemos
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    self.session_data = json.load(f)
                    return self.session_data
            
            return None
            
        except Exception as e:
            print(f"Error al cargar sesión: {e}")
            return None
    
    def get_role(self) -> str:
        """
        Obtiene el rol del usuario actual
        
        Returns:
            str: El rol del usuario (ej: 'admin', 'cashier', 'supervisor'), 
                 o None si no hay sesión activa
        """
        session = self.load_session()
        if session and 'role' in session:
            return session['role']
        return None
    
    def get_user_data(self) -> dict:
        """
        Obtiene todos los datos del usuario actual
        
        Returns:
            dict: Diccionario con todos los datos del usuario, o None si no hay sesión
        """
        return self.load_session()
    
    def has_module_access(self, module_number: int) -> bool:
        """
        Verifica si el usuario actual tiene acceso a un módulo específico
        
        Args:
            module_number (int): Número del módulo (1=Inicio, 2=Buscar, 3=Inventario, 
                                4=Empleados, 5=Balance, 6=Ajustes)
        
        Returns:
            bool: True si el usuario tiene acceso, False en caso contrario
        """
        role = self.get_role()
        
        if not role:
            return False
        
        # Definir los módulos permitidos para cada rol
        # module_number: 1=Inicio, 2=Buscar, 3=Inventario, 4=Empleados, 5=Balance, 6=Ajustes
        role_permissions = {
            "admin": [1, 2, 3, 4, 5, 6],  # Acceso completo a todos los módulos
            "supervisor": [1, 2, 3],  # Acceso limitado: Inicio, Buscar, Inventario
            "warehouse_manager": [1, 2, 3],  # Acceso limitado: Inicio, Buscar, Inventario
            "accountant": [1, 2, 3, 5],  # Acceso: Inicio, Buscar, Inventario, Balance
            "inventory_staff": [1, 2, 3],  # Acceso limitado: Inicio, Buscar, Inventario
            "cashier": [1, 2, 3],  # Acceso limitado: Inicio, Buscar, Inventario
            "stock_clerk": [1, 2, 3],  # Acceso limitado: Inicio, Buscar, Inventario
        }
        
        # Obtener los módulos permitidos para este rol
        allowed_modules = role_permissions.get(role, [])
        
        # Verificar si el módulo solicitado está en la lista de permitidos
        return module_number in allowed_modules
    
    def clear_session(self):
        """
        Elimina la sesión actual (cierre de sesión)
        """
        try:
            # Eliminar el archivo de sesión si existe
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            
            # Limpiar los datos en memoria
            self.session_data = None
            
        except Exception as e:
            print(f"Error al limpiar sesión: {e}")
    
    def is_logged_in(self) -> bool:
        """
        Verifica si hay una sesión activa
        
        Returns:
            bool: True si hay una sesión activa, False en caso contrario
        """
        return self.load_session() is not None


# Instancia global del SessionManager para usar en toda la aplicación
session_manager = SessionManager()

# Funciones de conveniencia para mantener compatibilidad con el código existente
def save_session(user_data: dict):
    """
    Función de conveniencia para guardar la sesión
    Usa la instancia global de SessionManager
    """
    session_manager.save_session(user_data)

def load_session() -> dict:
    """
    Función de conveniencia para cargar la sesión
    Usa la instancia global de SessionManager
    """
    return session_manager.load_session()


    