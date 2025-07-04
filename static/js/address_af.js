const addressInput = document.getElementById('address');
const suggestionsBox = document.getElementById('suggestions');

let debounce;
addressInput.addEventListener('input', () => {
    clearTimeout(debounce);
    const q = addressInput.value.trim();
    if (q.length < 3) {
        suggestionsBox.innerHTML = '';
        return;
    }

    debounce = setTimeout(() => {
        fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(q)}&apiKey=21576e6c288144af90743449e8420ec7`)
            .then(r => r.json())
            .then(data => {
                suggestionsBox.innerHTML = '';
                data.features.forEach(feature => {
                    const props = feature.properties;
                    const d = document.createElement('div');
                    d.className = 'autocomplete-suggestion';
                    d.textContent = props.formatted;
                    d.onclick = () => {
                        addressInput.value = props.formatted;
                        document.getElementById('address_line1').value = props.address_line1 || '';
                        document.getElementById('address_line2').value = props.street || 'NA';
                        document.getElementById('location').value = props.lat+','+ props.lon || 'NA';
                        document.getElementById('city').value = props.city || '';
                        document.getElementById('state').value = props.state || '';
                        document.getElementById('pincode').value = props.postcode || '';
                        document.getElementById('country').value = props.country || '';
                        suggestionsBox.innerHTML = '';
                    };
                    suggestionsBox.appendChild(d);
                });
            })
            .catch(err => {
                console.error('Geoapify error:', err);
                suggestionsBox.innerHTML = '<div class="error">Error fetching suggestions</div>';
            });
    }, 300);
});

document.addEventListener('click', (e) => {
    if (!addressInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.innerHTML = '';
    }
});
