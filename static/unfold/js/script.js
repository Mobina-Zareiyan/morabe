document.addEventListener('DOMContentLoaded', async () => {
    const header = document.querySelector('div.flex.flex-row.grow.font-semibold.items-center');
    if (!header) return;

    const walletBtn = document.createElement('a');
    walletBtn.href = '#'; // temporary, will update from API
    walletBtn.className = 'cursor-pointer flex items-center gap-2 px-3 py-1 text-sm font-semibold';
    
    // Styling for button-like appearance and right alignment
    // Button styles
    Object.assign(walletBtn.style, {
        background: 'transparent',
        border: '0.05rem solid var(--color-primary-600, #e5e7eb)',
        borderRadius: '0.375rem',
        padding: '0.5rem 0.75rem',
        height: '40px',
        fontSize: '0.855rem',
        color: `var(--muted-foreground)`,
        textDecoration: 'none',
        transition: 'all 0.2s ease',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
    });

    walletBtn.onmouseover = () => {
        walletBtn.style.background = 'transparent';
        walletBtn.style.border = '0.07rem solid rgba(152, 51, 147)';
        walletBtn.style.color = `var(--muted-foreground)`; 
    };
    walletBtn.onmouseout = () => {
        walletBtn.style.background = 'transparent';
        walletBtn.style.border= '0.05rem solid var(--color-primary-600, #e5e7eb)';
        walletBtn.style.color = `var(--muted-foreground)`; 
    };

    walletBtn.innerHTML = `
        <span class="material-symbols-outlined">wallet</span>
        کیف پول: loading...
    `;

    // Wrapper for absolute positioning
    const wrapper = document.createElement('div');
    wrapper.style.position = 'absolute';
    wrapper.style.top = '50%';
    wrapper.style.transform = 'translateY(-50%)';

    // Detect text direction
    const dir = getComputedStyle(header).direction || 'ltr';
    if (dir === 'rtl') {
        wrapper.style.left = '1rem';
    } else {
        wrapper.style.right = '1rem';
    }

    wrapper.appendChild(walletBtn);

    // Ensure header is relative
    if (getComputedStyle(header).position === 'static') {
        header.style.position = 'relative';
    }

    header.appendChild(wrapper);

    try {
        const res = await fetch('/contino/admin/my_wallet/', {
            headers: { 'Accept': 'application/json' },
            credentials: 'same-origin',
        });

        console.log('Raw response:', res);

        const text = await res.text();
        console.log('Response text:', text);

        let data;
        try {
            data = JSON.parse(text);
            console.log('Parsed data:', data);
        } catch (err) {
            console.error('Failed to parse JSON:', err);
            throw err;
        }


        var balance = data.data.balance;
        var formated = Intl.NumberFormat('en-US', { maximumFractionDigits:0, style: "currency", currency: "IRT" }).format(balance);
        walletBtn.innerHTML = `<span class="material-symbols-outlined">wallet</span> کیف پول: ${formated}`;
        if (data.url) {
            walletBtn.href = `${data.url}#transactions`; 
        }
    } catch (err) {
        console.error('Failed to load wallet balance', err);
        walletBtn.innerHTML = `<span class="material-symbols-outlined">wallet</span> کیف پول: error`;
        walletBtn.href = `${data.url}#transactions`;
    }
});


document.addEventListener('DOMContentLoaded', () => {
    console.log('[🟣 Chart Init] DOM fully loaded.');

    const canvas = document.getElementById('dashboardPieChart');
    if (!canvas) {
        console.error('[❌ Chart Error] Canvas element with id="dashboardPieChart" not found!');
        return;
    }

    console.log('[🟣 Chart Init] Found canvas:', canvas);

    const rawData = canvas.getAttribute('data-value');
    if (!rawData) {
        console.error('[❌ Chart Error] No data-value attribute found on canvas.');
        return;
    }

    console.log('[🟣 Chart Data Raw]', rawData);

    let data;
    try {
        data = JSON.parse(rawData.replace(/&quot;/g, '"'));
        console.log('[🟣 Chart Data Parsed]', data);
    } catch (err) {
        console.error('[❌ Chart Error] Failed to parse data-value JSON:', err);
        return;
    }

    // Assign purple colors
    data.datasets[0].backgroundColor = [
        '#59168b',
        '#8200db',
        '#ad46ff',
        '#dab2ff',
    ];

    console.log('[🟣 Chart Configured Data]', data);

    try {
        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.error('[❌ Chart Error] Could not get 2D context from canvas.');
            return;
        }

        console.log('[🟣 Chart Init] Creating chart instance...');
        new Chart(ctx, {
            type: 'pie',
            data: data,
            options: { 
                responsive: true, 
                maintainAspectRatio: false 
            }
        });
        console.log('[✅ Chart Success] Chart rendered successfully!');
    } catch (err) {
        console.error('[❌ Chart Error] Failed to initialize chart:', err);
    }
});

function hideRuTabs() {
    console.log("[Admin Tabs] Attempting to hide all RU tabs...");

    const ruTabs = document.querySelectorAll('li[aria-controls$="_ru"]');
    const ruContents = document.querySelectorAll('[id$="_ru"]');

    if (ruTabs.length === 0 || ruContents.length === 0) {
        
        setTimeout(hideRuTabs, 100); // retry in 100ms
        return;
    }

    ruTabs.forEach(tab => {
        tab.style.display = 'none';
        
    });

    ruContents.forEach(content => {
        content.style.display = 'none';
        
    });

}

// run after DOM ready
document.addEventListener("DOMContentLoaded", hideRuTabs);




