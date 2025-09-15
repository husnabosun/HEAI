const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('main-container');
const API_URL = "/ai_treatment/";

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
			treatmentContainer.querySelector('.sign-in-container').innerHTML = 'Yükleniyor...';
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
				<h3>AI Tedavi Önerileri</h3>
				<ul>${data.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>`;
				responseLoaded=true;
			} catch (err) {
				treatmentContainer.querySelector('.sign-in-container').innerHTML = 'AI cevabı alınamadı.';
				console.error(err);
			}
	});


	document.addEventListener("DOMContentLoaded", function() {
    fetch('/trend_data/')  // Django view endpoint
      .then(res => res.json())
      .then(data => {
        const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];

        // Hastalık grafiği
        new Chart(document.getElementById('diseaseChart').getContext('2d'), {
          type: 'line',
          data: {
            labels: data.dates,
            datasets: Object.keys(data.disease_counts).map((d, i) => ({
              label: d,
              data: data.disease_counts[d],
              borderColor: colors[i % colors.length],
              fill: false,
            }))
          },
          options: { responsive: true, plugins: { title: { display: true, text: 'Hastalık Trendleri (Haftalık)' } } }
        });

        // Branş grafiği
        new Chart(document.getElementById('branchChart').getContext('2d'), {
          type: 'line',
          data: {
            labels: data.dates,
            datasets: Object.keys(data.branch_counts).map((b, i) => ({
              label: b,
              data: data.branch_counts[b],
              borderColor: colors[i % colors.length],
              fill: false,
            }))
          },
          options: { responsive: true, plugins: { title: { display: true, text: 'Branş Trendleri (Haftalık)' } } }
        });

        // Semptom grafiği
        new Chart(document.getElementById('symptomChart').getContext('2d'), {
          type: 'line',
          data: {
            labels: data.dates,
            datasets: Object.keys(data.symptom_counts).map((s, i) => ({
              label: s,
              data: data.symptom_counts[s],
              borderColor: colors[i % colors.length],
              fill: false,
            }))
          },
          options: { responsive: true, plugins: { title: { display: true, text: 'Semptom Trendleri (Haftalık)' } } }
        });
    });
});



}


