'use strict';

function modalShown(event) {
    let button = event.relatedTarget;
    let recipeId = button.dataset.recipeId;
    let feedbackId = button.dataset.feedbackId;
    let newUrl = `/recipes/${recipeId}/feedback/${feedbackId}/delete`;
    let form = document.getElementById('deleteModalForm');
    form.action = newUrl;
}

let modal = document.getElementById('deleteModal');
modal.addEventListener('show.bs.modal', modalShown);