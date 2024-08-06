document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('input_titulo_proyecto').addEventListener('input', function(){
        document.getElementById('tiutlo_proyecto').innerText = this.value;
    });  
    const modal_crear_proyecto = document.getElementById('id_modal_crear_proyecto');
    const btn_abrir_modal_crear_proyecto = document.getElementById('abrir_modal_crear_proyecto');
    const btn_cancelar_proyecto = document.getElementById('btn_cancelar_proyecto');
    btn_abrir_modal_crear_proyecto.addEventListener('click', () =>{
        modal_crear_proyecto.classList.add('mostrar_modal_crear_proyecto');
    })
    btn_cancelar_proyecto.addEventListener('click', () =>{
        modal_crear_proyecto.classList.remove('mostrar_modal_crear_proyecto');
    })
});


// inicio ELIMINAR OFICIO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_oficio');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_oficio');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_oficio');
        });
    });
});
// fin ELIMINAR OFICIO



// inicio EDITAR MATERIALCONCEPTO
// fin EDITAR MATERIALCONCEPTO

// inicio ELIMINAR MATERIALCONCEPTO
// fin ELIMINAR MATERIALCONCEPTO


// inicio EDITAR MATERIALCONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_editar_materialconcepto');
    const modals = document.querySelectorAll('.modal_editar_materialconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_editar_materialconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_editar_materialconcepto');
        });
    });
});
// fin EDITAR MATERIALCONCEPTO

// inicio ELIMINAR MATERIALCONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_materialconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_materialconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_materialconcepto');
        });
    });
});
// fin ELIMINAR MATERIALCONCEPTO




// inicio EDITAR MAQUINARIACONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_editar_maquinariaconcepto');
    const modals = document.querySelectorAll('.modal_editar_maquinariaconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_editar_maquinariaconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_editar_maquinariaconcepto');
        });
    });
});
// fin EDITAR MAQUINARIACONCEPTO

// inicio ELIMINAR MAQUINARIACONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_maquinariaconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_maquinariaconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_maquinariaconcepto');
        });
    });
});
// fin ELIMINAR MAQUINARIACONCEPTO



// inicio REGISTRAR CONCEPTO
document.addEventListener('DOMContentLoaded', () => {
    const modalRegistrarConcepto = document.getElementById('registrar_concepto');
    const btnAbrirModalRegistrarConcepto = document.querySelector('.btn_registrar[href="#registrar_concepto"]');
    const btnCancelarRegistrarConcepto = document.getElementById('btn_cancelar_registrar_concepto');
    if (btnAbrirModalRegistrarConcepto) {
        btnAbrirModalRegistrarConcepto.addEventListener('click', (event) => {
            event.preventDefault();
            modalRegistrarConcepto.classList.add('show');
        });
    }
    if (btnCancelarRegistrarConcepto) {
        btnCancelarRegistrarConcepto.addEventListener('click', (event) => {
            event.preventDefault();
            modalRegistrarConcepto.classList.remove('show');
        });
    }
});

// fin REGISTRAR CONCEPTO

// inicio ELIMINAR CONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_concepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_concepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_concepto');
        });
    });
});
// fin ELIMINAR CONCEPTO

// inicio EDITAR PROYECTO
document.addEventListener('DOMContentLoaded', () => {
    const modalEditarProyecto = document.getElementById('editar_proyecto');
    const btnAbrirModalEditarProyecto = document.querySelector('.btn_registrar[href="#editar_proyecto"]');
    const btnCancelarEditarProyecto = document.getElementById('btn_cancelar_editar_proyecto');
    if (btnAbrirModalEditarProyecto) {
        btnAbrirModalEditarProyecto.addEventListener('click', (event) => {
            event.preventDefault();
            modalEditarProyecto.classList.add('show');
        });
    }
    if (btnCancelarEditarProyecto) {
        btnCancelarEditarProyecto.addEventListener('click', (event) => {
            event.preventDefault();
            modalEditarProyecto.classList.remove('show');
        });
    }
});
// fin EDITAR PROYECTO

// -----// inicio BUSQUEDA MATERIALES //-----
document.getElementById('searchBoxmats').addEventListener('input', function() {
    var query = this.value.toLowerCase();
    var results = document.querySelectorAll('#resultsmats .resultmats');
    var resultsContainer = document.getElementById('resultsmats');
    var hasVisibleResults = false;

    results.forEach(function(result) {
        var text = result.textContent.toLowerCase();
        if (text.includes(query)) {
            result.classList.remove('hiddenmats');
            hasVisibleResults = true;
        } else {
            result.classList.add('hiddenmats');
        }
    });

    if (query.length > 0 && hasVisibleResults) {
        resultsContainer.style.display = 'block';
    } else {
        resultsContainer.style.display = 'none';
    }
});

document.getElementById('searchBoxmats').addEventListener('focus', function() {
    if (this.value.length > 0) {
        document.getElementById('resultsmats').style.display = 'block';
    }
});

document.getElementById('searchBoxmats').addEventListener('blur', function() {
    setTimeout(function() {
        document.getElementById('resultsmats').style.display = 'none';
    }, 200);
});

document.getElementById('resultsmats').addEventListener('mousedown', function(e) {
    e.preventDefault();
});
// -----// fin BUSQUEDA MATERIALES //-----

// -----// inicio BUSQUEDA MAQUINARIA //-----
document.getElementById('searchBoxmaqs').addEventListener('input', function() {
    var query = this.value.toLowerCase();
    var results = document.querySelectorAll('#resultsmaqs .resultmaqs');
    var resultsContainer = document.getElementById('resultsmaqs');
    var hasVisibleResults = false;

    results.forEach(function(result) {
        var text = result.textContent.toLowerCase();
        if (text.includes(query)) {
            result.classList.remove('hiddenmaqs');
            hasVisibleResults = true;
        } else {
            result.classList.add('hiddenmaqs');
        }
    });

    if (query.length > 0 && hasVisibleResults) {
        resultsContainer.style.display = 'block';
    } else {
        resultsContainer.style.display = 'none';
    }
});

document.getElementById('searchBoxmaqs').addEventListener('focus', function() {
    if (this.value.length > 0) {
        document.getElementById('resultsmaqs').style.display = 'block';
    }
});

document.getElementById('searchBoxmaqs').addEventListener('blur', function() {
    setTimeout(function() {
        document.getElementById('resultsmaqs').style.display = 'none';
    }, 200);
});

document.getElementById('resultsmaqs').addEventListener('mousedown', function(e) {
    e.preventDefault();
});
// -----// fin BUSQUEDA MAQUINARIA //-----