'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let recipeId = button.dataset.recipeId;
    let recipeName = button.dataset.recipeName;
    let newUrl = `/recipes/${recipeId}/delete`;
    let form = document.getElementById('deleteModalForm');
    form.action = newUrl;
    document.querySelector('.modal-body').textContent = `Вы уверены, что хотите удалить рецепт "${recipeName}?"`;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);