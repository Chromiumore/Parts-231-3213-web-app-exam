'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let recipeId = button.dataset.recipeId;
    let newUrl = `/recipes/${recipeId}/delete`;
    let form = document.getElementById('deleteModalForm');
    form.action = newUrl;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);