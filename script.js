$(document).ready(
    function () {

        document.getElementById("elements-add")?.addEventListener("submit", function (event) { // ? prevents entry into this block if id is null
            event.preventDefault(); // does not enter /add url due to prevention of default behaviour 
	    // adding element name using document.getElementById which retrieves information from id
            var element_name = document.getElementById("element_name").value;

            // adding element code using document.getElementById which retrieves information from id
            var element_code = document.getElementById("element_code").value;

            // adding element number using document.getElementById which retrieves information from id
            var element_no = document.getElementById("element_no").value;

            // adding element colour1 using document.getElementById which retrieves information from id
            var colour1 = document.getElementById("element_colour_one").value;

            // adding element colour2 using document.getElementById which retrieves information from id
            var colour2 = document.getElementById("element_colour_two").value;

            // adding element colour3 using document.getElementById which retrieves information from id
            var colour3 = document.getElementById("element_colour_three").value;

            // adding element radius using document.getElementById which retrieves information from id
            var radius = document.getElementById("radius").value;

            $('#element_no option:selected').remove(); // removing selected element no from dropdown list
            $('#element_name option:selected').remove(); // removing selected element name from dropdown list
	    $('#element_code option:selected').remove(); // removing selected element code from dropdown list


            $.post("/add", {
                element_name: element_name, // posting element_name
                element_code: element_code, // posting element_code
                element_no: element_no,
                colour1: colour1,
                colour2: colour2,
                colour3: colour3,
                radius: radius
            }, function (data, status) {
                alert("Data: " + data + "\nStatus: " + status);
            });
        });

        document.getElementById("remove-element")?.addEventListener("submit", function (event) {
            event.preventDefault();
            var element_no = document.getElementById("rm_element_no").value;

            $.post("/remove", {
                element_no: element_no
            }, function (data, status) {
                alert("Data: " + data + "\nStatus: " + status);
            });

        });

        document.getElementById("sdf_form")?.addEventListener("submit", function (event) {
            event.preventDefault();
            var file_input = document.getElementById("sdf_file"); // getting the file
            var file_array = file_input.value.split("\\")[2]; // splitting the code
            var file_name = file_array.split(".sdf")[0]; // splitting further to remove trash
            var sdf_file = document.getElementById("sdf_form");
            var formData = new FormData()
            formData.append(file_name, file_input.files[0]) // for sending to the server
            $.ajax({
                url: '/sdf',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log(response);
                
                }
            });

        });
    }
);