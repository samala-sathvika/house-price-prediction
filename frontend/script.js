async function predictPrice() {

    // Get input values
    const area = document.getElementById("area").value;
    const bedrooms = document.getElementById("bedrooms").value;
    const bathrooms = document.getElementById("bathrooms").value;
    const age = document.getElementById("age").value;

    // Check empty fields
    if (
        area === "" ||
        bedrooms === "" ||
        bathrooms === "" ||
        age === ""
    ) {
        alert("Please enter all house details.");
        return;
    }

    // Convert values to numbers
    const houseData = {
        area: Number(area),
        bedrooms: Number(bedrooms),
        bathrooms: Number(bathrooms),
        age: Number(age)
    };

    // Show loading
    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    try {

        // Send data to FastAPI
        const response = await fetch(
            "/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(houseData)
            }
        );

        // Check response
        if (!response.ok) {
            throw new Error("Prediction failed");
        }

        // Convert response to JSON
        const data = await response.json();

        // Format price
        const formattedPrice =
            new Intl.NumberFormat(
                "en-IN",
                {
                    style: "currency",
                    currency: "INR",
                    maximumFractionDigits: 0
                }
            ).format(data.predicted_price);

        // Display result
        document.getElementById("price").textContent =
            formattedPrice;

        document.getElementById("result").style.display =
            "block";

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the FastAPI server. " +
            "Make sure the backend is running."
        );

    }

    finally {

        document.getElementById("loading").style.display =
            "none";
    }
}