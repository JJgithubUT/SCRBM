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


// inicio ELIMINAR UNIDAD
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_unidad');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_unidad');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_unidad');
        });
    });
});
// fin ELIMINAR UNIDAD

// inicio ELIMINAR MATERIAL
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_material');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_material');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_material');
        });
    });
});
// fin ELIMINAR MATERIAL

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

// inicio ELIMINAR MAQUINARIA
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_maquinaria');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_maquinaria');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_maquinaria');
        });
    });
});
// fin ELIMINAR MAQUINARIA



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

// inicio REGISTRAR MAQUINARIACONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_avanzar');
    const modals = document.querySelectorAll('.modal_registrar_maquinariaconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_registrar_maquinariaconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_registrar_maquinariaconcepto');
        });
    });
});
// fin REGISTRAR MAQUINARIACONCEPTO

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

// inicio ELIMINAR BASICOCONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_basicoconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_basicoconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_basicoconcepto');
        });
    });
});
// fin ELIMINAR BASICOCONCEPTO

// inicio ELIMINAR OFICIOCONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_oficioconcepto');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_oficioconcepto');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_oficioconcepto');
        });
    });
});
// fin ELIMINAR OFICIOCONCEPTO


// inicio REGISTRAR BASICO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_registrar');
    const modals = document.querySelectorAll('.modal_registrar_basico');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_registrar_basico');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_registrar_basico');
        });
    });
});
// fin REGISTRAR BASICO

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



// inicio EDITAR BASICO
document.addEventListener('DOMContentLoaded', () => {
    const modalRegistrarConcepto = document.getElementById('editar_basico');
    const btnAbrirModalRegistrarConcepto = document.querySelector('.btn_registrar[href="#editar_basico"]');
    const btnCancelarRegistrarConcepto = document.getElementById('btn_cancelar_editar_basico');
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

// fin EDITAR BASICO


//DERIVA DE BASICO LO DE ABAJO DERIVA DE BASICO LO DE ABAJO     
// inicio EDITAR CONCEPTO
document.addEventListener('DOMContentLoaded', () => {
    const modalRegistrarConcepto = document.getElementById('editar_concepto');
    const btnAbrirModalRegistrarConcepto = document.querySelector('.btn_registrar[href="#editar_concepto"]');
    const btnCancelarRegistrarConcepto = document.getElementById('btn_cancelar_editar_concepto');
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

// fin EDITAR CONCEPTO





// inicio ELIMINAR MATERIALBASICO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_materialbasico');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_materialbasico');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_materialbasico');
        });
    });
});
// fin ELIMINAR MATERIALBASICO

// inicio ELIMINAR MATERIALCONCEPTO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_oficiobasico');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_oficiobasico');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_oficiobasico');
        });
    });
});
// fin ELIMINAR MATERIALCONCEPTO

// inicio ELIMINAR BASICO
document.addEventListener('DOMContentLoaded', (event) => {
    const eliminarButtons = document.querySelectorAll('.btn_eliminar');
    const modals = document.querySelectorAll('.modal_eliminar_basico');

    eliminarButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modalId = button.getAttribute('href').substring(1);
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('mostrar_modal_eliminar_basico');
            }
        });
    });

    modals.forEach(modal => {
        const cancelButton = modal.querySelector('a[href="#"]');
        cancelButton.addEventListener('click', (event) => {
            event.preventDefault();
            modal.classList.remove('mostrar_modal_eliminar_basico');
        });
    });
});
// fin ELIMINAR BASICO