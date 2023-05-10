// PARA IMAGEM NO FORM
function readImgURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#boardgame_image')
                .attr('src', e.target.result)
        };
        reader.readAsDataURL(input.files[0]);
    }
}