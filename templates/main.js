'use strict';

console.log("JS started");
$(document).ready(function () {
    // jQuery methods go here...
    const subfolder = $("#subfolder").attr("value")
    const num_letters = parseInt($("#num_letters").attr("value"), 10)
    var img_id = Math.floor(Math.random() * num_letters);
    console.log("Document ready", subfolder, "num_letters", num_letters, "img_id", img_id);

    function next_img() {
        img_id = (img_id + 1) % num_letters;
        var image_path = './imgs/' + subfolder + '/' + img_id + '.png'
        $("#hint-img").attr("src", image_path)
        console.log("click", img_id, image_path);
    }

    $("#hint-img").click(next_img);
    $("#button-next").click(next_img);

    next_img()
})