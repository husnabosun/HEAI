const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

if (signUpButton) {
	signUpButton.addEventListener('click', () => {
		container.classList.add("right-panel-active");
	});
}

if (signInButton) {
	signInButton.addEventListener('click', () => {
		container.classList.remove("right-panel-active");
	});
}

const sidebar = document.querySelector('.sidebar-buttons');
if (sidebar) {
	sidebar.style.height = container.offsetHeight + 'px';

	const buttons = document.querySelectorAll('.sidebar-buttons button');

	buttons.forEach(btn => {
		btn.addEventListener('mouseenter', (e) => {
			const tooltipText = btn.getAttribute('data-tooltip');
			const tooltip = document.createElement('div');
			tooltip.className = 'tooltip-js';
			tooltip.innerText = tooltipText;
			document.body.appendChild(tooltip);

			const rect = btn.getBoundingClientRect();
			tooltip.style.left = rect.right + 10 + 'px';
			tooltip.style.top = rect.top + window.scrollY + (rect.height / 2) - (tooltip.offsetHeight / 2) + 'px';
			tooltip.style.opacity = 1;

			btn._tooltip = tooltip;
		});

		btn.addEventListener('mouseleave', () => {
			if (btn._tooltip) {
				btn._tooltip.remove();
				btn._tooltip = null;
			}
		});
	});

	const btnTreatment = document.getElementById('treatment');
	const treatmentContainer = document.getElementById('treatment-response');

	btnTreatment.addEventListener('click', async () => {
		const diseaseElements = document.querySelectorAll('#disease-p');
		const diseases = Array.from(diseaseElements)
			.map(p => p.innerText.split('\n')[0].replace('Hastalık : ', ''));

		if (diseases.length === 0) {
			alert("Hastalık bilgisi yok!");
			return;
		}

		treatmentContainer.style.display = 'block';
		treatmentContainer.querySelector('.sign-in-container').innerHTML = 'Yükleniyor...';

		try {
			const response = await fetch('/ai-endpoint/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': '{{ csrf_token }}'
				},
				body: JSON.stringify({ diseases: diseases })
			});
			const data = await response.json();

			treatmentContainer.querySelector('.sign-in-container').innerHTML = `
            <h3>AI Tedavi Önerileri</h3>
            <ul>${data.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>
        `;
		} catch (err) {
			treatmentContainer.querySelector('.sign-in-container').innerHTML = 'AI cevabı alınamadı.';
			console.error(err);
		}
	});



}
