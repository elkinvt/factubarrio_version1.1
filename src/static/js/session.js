function cerrarSesion() {
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = '/cerrar_sesion';
}
