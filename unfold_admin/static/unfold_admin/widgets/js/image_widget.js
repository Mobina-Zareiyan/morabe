function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var inputInputId = input.id;
            document.getElementById(`img-preview-section-${inputInputId}`).classList.remove('hidden');
            document.getElementById(`img-preview-${inputInputId}`).src = e.target.result;
            document.getElementById(`img-preview-link-${inputInputId}`).href = e.target.result;
            document.getElementById(`img-preview-link-${inputInputId}`).classList.remove('hidden');
        };

        reader.readAsDataURL(input.files[0]);
    }
}