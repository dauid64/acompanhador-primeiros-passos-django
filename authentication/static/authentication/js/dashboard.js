$(document).ready(function () {
    // Configuração inicial
    const ANIMATION_DURATION = 1000;
    const PROGRESS_DELAY = 300;
    
    // Função utilitária para animar números
    function animateNumber(element, finalValue, duration = 1000, suffix = '%') {
        const startValue = 0;
        const increment = finalValue / (duration / 16); // 60fps
        let currentValue = startValue;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                currentValue = finalValue;
                clearInterval(timer);
            }
            element.textContent = Math.round(currentValue) + suffix;
        }, 16);
    }
    
    // Função para animar círculo de progresso
    function animateCircularProgress() {
        const progressRing = $('.progress-ring-fill');
        if (progressRing.length) {
            const progressValue = parseFloat(progressRing.data('progress')) || 0;
            const circumference = 327; // 2 * π * r (r = 52)
            const offset = circumference - (progressValue / 100) * circumference;
            
            setTimeout(() => {
                progressRing.css('stroke-dashoffset', offset);
            }, PROGRESS_DELAY);
            
            // Animar o número no centro
            const progressText = $('.progress-percentage');
            if (progressText.length) {
                setTimeout(() => {
                    animateNumber(progressText[0], progressValue, ANIMATION_DURATION);
                }, PROGRESS_DELAY + 500);
            }
        }
    }
    
    // Função para animar barras de progresso modernas
    function animateProgressBars() {
        $('.modern-progress-fill').each(function(index) {
            const $bar = $(this);
            const progress = parseFloat($bar.data('progress')) || 0;
            
            // Adicionar classe de loading
            $bar.parent().addClass('loading');
            
            setTimeout(() => {
                $bar.css('width', progress + '%');
                
                // Remover loading após animação
                setTimeout(() => {
                    $bar.parent().removeClass('loading');
                }, ANIMATION_DURATION);
            }, PROGRESS_DELAY + (index * 100));
        });
    }
    
    // Função para animar barras de progresso legadas (compatibilidade)
    function animateLegacyProgressBars() {
        $('.progress-bar').each(function(index) {
            const $container = $(this);
            const progress = parseFloat($container.data('progress'));
            
            if (!isNaN(progress)) {
                setTimeout(() => {
                    $container.find('.progress').css('width', progress + '%');
                }, PROGRESS_DELAY + (index * 100));
            }
        });
    }
    
    // Função para adicionar efeitos de entrada escalonados
    function addStaggeredEntryAnimations() {
        $('.chapter-card').each(function(index) {
            $(this).css({
                'animation-delay': (index * 0.1) + 's'
            }).addClass('fade-in-up');
        });
    }
    
    // Função para adicionar interatividade nos cards
    function addCardInteractivity() {
        $('.chapter-card').on('mouseenter', function() {
            $(this).find('.modern-progress-fill').css('animation-play-state', 'paused');
        }).on('mouseleave', function() {
            $(this).find('.modern-progress-fill').css('animation-play-state', 'running');
        });
        
        // Adicionar efeito de clique
        $('.chapter-card').on('click', function(e) {
            // Se não clicou no botão, redirecionar
            if (!$(e.target).closest('.chapter-btn').length) {
                const link = $(this).find('.chapter-btn').attr('href');
                if (link) {
                    window.location.href = link;
                }
            }
        });
    }
    
    // Função para observar elementos na viewport (Intersection Observer)
    function setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            const observerOptions = {
                threshold: 0.2,
                rootMargin: '50px'
            };
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const $element = $(entry.target);
                        
                        if ($element.hasClass('progress-ring-fill')) {
                            animateCircularProgress();
                        } else if ($element.hasClass('chapter-card')) {
                            $element.addClass('animate-in');
                        }
                        
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);
            
            // Observar elementos relevantes
            $('.progress-ring-fill, .chapter-card').each(function() {
                observer.observe(this);
            });
        } else {
            // Fallback para navegadores antigos
            setTimeout(() => {
                animateCircularProgress();
                addStaggeredEntryAnimations();
            }, 100);
        }
    }
    
    // Função para adicionar tooltips informativos
    function addTooltips() {
        $('.stat-item').each(function() {
            const $item = $(this);
            const text = $item.find('.stat-text').text();
            $item.attr('title', text);
        });
        
        $('.completion-badge').each(function() {
            const $badge = $(this);
            const text = $badge.text().trim();
            const descriptions = {
                'Quase completo!': 'Você está quase terminando este capítulo!',
                'Em progresso': 'Continue assim, você está indo bem!',
                'Iniciado': 'Ótimo começo, continue estudando!',
                'Não iniciado': 'Clique para começar este capítulo'
            };
            $badge.attr('title', descriptions[text] || text);
        });
    }
    
    // Função para melhorar a acessibilidade
    function enhanceAccessibility() {
        // Adicionar ARIA labels
        $('.progress-circle').attr('role', 'progressbar')
                            .attr('aria-label', 'Progresso geral do curso');
        
        $('.modern-progress-bar').each(function() {
            const progress = $(this).find('.modern-progress-fill').data('progress') || 0;
            $(this).attr('role', 'progressbar')
                   .attr('aria-valuenow', progress)
                   .attr('aria-valuemin', '0')
                   .attr('aria-valuemax', '100')
                   .attr('aria-label', `Progresso do capítulo: ${progress}%`);
        });
        
        // Melhorar navegação por teclado
        $('.chapter-card').attr('tabindex', '0').on('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                $(this).find('.chapter-btn')[0].click();
            }
        });
    }
    
    // Função para salvar preferências no localStorage
    function saveUserPreferences() {
        const preferences = {
            lastVisit: new Date().toISOString(),
            animationsEnabled: !window.matchMedia('(prefers-reduced-motion: reduce)').matches
        };
        
        localStorage.setItem('dashboardPreferences', JSON.stringify(preferences));
    }
    
    // Função para adicionar indicadores de performance
    function addPerformanceMetrics() {
        const startTime = performance.now();
        
        $(window).on('load', function() {
            const loadTime = performance.now() - startTime;
            console.log(`Dashboard carregado em ${loadTime.toFixed(2)}ms`);
            
            // Adicionar classe quando tudo estiver carregado
            $('body').addClass('dashboard-loaded');
        });
    }
    
    // Inicialização principal
    function initializeDashboard() {
        // Verificar se o usuário prefere animações reduzidas
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        if (!prefersReducedMotion) {
            // Inicializar animações
            setupIntersectionObserver();
            addStaggeredEntryAnimations();
        } else {
            // Aplicar estados finais imediatamente
            animateCircularProgress();
            $('.modern-progress-fill').each(function() {
                const progress = parseFloat($(this).data('progress')) || 0;
                $(this).css('width', progress + '%');
            });
        }
        
        // Inicializar funcionalidades sempre presentes
        animateProgressBars();
        animateLegacyProgressBars();
        addCardInteractivity();
        addTooltips();
        enhanceAccessibility();
        saveUserPreferences();
        addPerformanceMetrics();
        
        // Adicionar classe de inicialização completa
        setTimeout(() => {
            $('body').addClass('dashboard-initialized');
        }, 500);
    }
    
    // Executar inicialização
    initializeDashboard();
    
    // Adicionar listener para mudanças de preferência de movimento
    if (window.matchMedia) {
        const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
        mediaQuery.addListener(function() {
            location.reload(); // Recarregar para aplicar novas preferências
        });
    }
    
    // Debug mode (apenas em desenvolvimento)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.dashboardDebug = {
            animateCircularProgress,
            animateProgressBars,
            addStaggeredEntryAnimations
        };
        console.log('Dashboard Debug Mode ativado. Use window.dashboardDebug para acessar funções.');
    }
});