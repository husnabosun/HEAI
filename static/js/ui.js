const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('main-container');

const loginContainer = document.getElementById('container')

const overlaySignUp = document.getElementById('overlaySignUp');
const overlaySignIn = document.getElementById('overlaySignIn');

const API_URL = "/ai_treatment/";

if (signUpButton) {
	overlaySignUp.addEventListener('click', () => {
		loginContainer.classList.add("right-panel-active");
	});
}

if (signInButton) {
	overlaySignIn.addEventListener('click', () => {
		loginContainer.classList.remove("right-panel-active");
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
	let responseLoaded = false;

	btnTreatment.addEventListener('click', async () => {
		const diseaseElements = document.querySelectorAll('#disease-p');
		const diseases = Array.from(diseaseElements)
			.map(p => p.innerText.split('\n')[0].replace('Hastalık : ', ''));

		if (diseases.length === 0) {
			alert("Hastalık bilgisi yok!");
			return;
		}

		if (treatmentContainer.style.display === 'block') {
			treatmentContainer.style.display = 'none';
			container.style.display = 'block';
			return;
		}

		container.style.display = "none";
		treatmentContainer.style.display = 'block';
		if (!responseLoaded) {
			
			treatmentContainer.querySelector('.sign-in-container').innerHTML = `
        <div class="loading-container-t">
            <div class="loading-spinner-t"></div>
            <div class="loading-text-t">Yükleniyor...</div>
        </div>
    `;
		}

		try {
			const response = await fetch(API_URL, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ diseases: diseases })
			});
			const data = await response.json();

			treatmentContainer.querySelector('.sign-in-container').innerHTML = `
    <div class="treatment-modern-ui">
        <h2 class="treatment-header">
            <svg class="treatment-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
            </svg>
            AI Tedavi Önerileri
        </h2>
        <div class="treatment-box" style="width:800px;">
<div class="treatment-content">
${data.recommendations.join('<br><br>')}
</div>

        </div>
    </div>
`;
			responseLoaded = true;
		} catch (err) {
			treatmentContainer.querySelector('.sign-in-container').innerHTML = 'AI cevabı alınamadı.';
			console.error(err);
		}
	});






}
