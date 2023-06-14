$(document).ready(
    function () {
        $.ajax({
            url: '/select_molecule',
            type: 'GET',
            dataType: 'json',
            success: function (data) { // execute code within the bracket after receiving data back from the server
                console.log("received data"); // printing message in console
                var select_mol = $('#molecule-select') // the select bar
                molecule_data = data; // transferring the GET data into a global variable
                for (var i = 0; i < data.length; i++) {
                    var option = $('<option>');
                    var temp = data[i][0].replaceAll('"', '') // removing garbage characters
                    option.val(i)
                    option.text(temp)
                    select_mol.append(option)

                }
            }
        })
        document.getElementById("choose-molecule")?.addEventListener("submit", function (event) {
            event.preventDefault();
            var selected_option = $('#molecule-select').val(); // getting the selected option
            var atom_no = 0; // atom number in molecule
            var bond_no = 0; // bond number in molecule

            atom_no = molecule_data[selected_option][1]; // atom number of selected molecule
            bond_no = molecule_data[selected_option][2]; // bond number of selected molecule

            var response = prompt(`Molecule Name: ${molecule_data[selected_option][0]}\nNumber of Atoms: ${molecule_data[selected_option][1]}\nNumber of Bonds: ${molecule_data[selected_option][2]}`, "yes");

            if (response == null) { // if no response by user, go back
                console.log("Choosing another option")
            } else if (response == "yes") { // if user enters yes, display the molecule
                console.log(`choosing ${molecule_data[selected_option][0]}`);
                $.post("/option_selected", { // post method to send molecule name to POST method
                    molecule: molecule_data[selected_option][0]
                }, function (data, status) {
                    alert("Data: " + data + "\nStatus: " + status);

                    var string_svg = $('#svg-image');

                    string_svg.empty();

                    string_svg.append(data);
                })
            } else {
                console.log(`something went wrong`);
            }

        })
    }
)