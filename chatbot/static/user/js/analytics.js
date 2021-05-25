
// circle gradient
function proficiency(selector,percent) {
    var options = {
        chart: {
            height: 280,
            type: 'radialBar',
        },
        colors: ['#e8769f'],
        plotOptions: {
            radialBar: {
                startAngle: -135,
                endAngle: 225,
                    hollow: {
                    margin: 0,
                    size: '70%',
                    background: '#fff',
                    image: undefined,
                    imageOffsetX: 0,
                    imageOffsetY: 0,
                    position: 'front',

                    dropShadow: {
                        enabled: true,
                        top: 3,
                        left: 0,
                        blur: 4,
                        opacity: 0.24
                    }
                },
                track: {
                    background: '#fff',
                    strokeWidth: '67%',
                    margin: 0, // margin is in pixels
                    dropShadow: {
                        enabled: true,
                        top: -3,
                        left: 0,
                        blur: 4,
                        opacity: 0.35
                    }
                },

                dataLabels: {
                    showOn: 'always',
                    name: {
                        offsetY: -10,
                        show: true,
                        color: '#888',
                        fontSize: '17px'
                    },
                    value: {
                        /* formatter: function(val) {
                            return parseInt(val);
                        }, */
                        color: '#111',
                        fontSize: '36px',
                        show: true,
                    }
                }
            }
        },
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'dark',
                type: 'horizontal',
                shadeIntensity: 0.5,
                gradientToColors: ['#5a5278'],
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 100]
            }
        },
        series: [percent],
        stroke: {
            lineCap: 'round'
        },
        labels: ['Proficiency'],
    }

    var chart = new ApexCharts(
        document.querySelector(selector),
        options
    );

    chart.render();    
}

function responseTime(selector, time) {
    
    let percent = time['avg']/time['max']*100
    var options = {
        chart: {
            height: 280,
            type: 'radialBar',
        },
        colors: ['#999'],
        plotOptions: {
            radialBar: {
                startAngle: -135,
                endAngle: 225,
                    hollow: {
                    margin: 0,
                    size: '70%',
                    background: '#fff',
                    image: undefined,
                    imageOffsetX: 0,
                    imageOffsetY: 0,
                    position: 'front',

                    dropShadow: {
                        enabled: true,
                        top: 3,
                        left: 0,
                        blur: 4,
                        opacity: 0.24
                    }
                },
                track: {
                    background: '#fff',
                    strokeWidth: '67%',
                    margin: 0, // margin is in pixels
                    dropShadow: {
                        enabled: true,
                        top: -3,
                        left: 0,
                        blur: 4,
                        opacity: 0.35
                    }
                },

                dataLabels: {
                    showOn: 'always',
                    name: {
                        offsetY: -10,
                        show: true,
                        color: '#888',
                        fontSize: '17px'
                    },
                    value: {
                        formatter: function(val) {
                            return Math.round( ( time['avg'] + Number.EPSILON ) * 100 ) / 100+'ms';
                        },
                        color: '#111',
                        fontSize: '25px',
                        show: true,
                    }
                }
            }
        },
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'dark',
                type: 'horizontal',
                shadeIntensity: 0.5,
                gradientToColors: ['#ccc'],
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 100]
            }
        },
        series: [percent],
        stroke: {
            lineCap: 'round'
        },
        labels: ['Response Time'],
    }

    var chart = new ApexCharts(
        document.querySelector(selector),
        options
    );

    chart.render();    
}

function messagesPerDay(selector, data) {
    console.log(JSON.parse(data,JSON.dateParser))
    var options = {
        title: {
            text: "Messages Count",
            align: 'bottom',
        },
        chart: {
            height: 300,
            type: 'area',
            stacked: true,
            toolbar: {
                show: true,
                offsetX: 0,
                offsetY: 0,
                tools: {
                download: false,
                selection: true,
                zoom: true,
                zoomin: true,
                zoomout: true,
                pan: true,
                reset: '<i class="fas fa-sync-alt"></i>',
                customIcons: []
                },
                autoSelected: 'pan',
            },
            events: {
                selection: function(chart, e) {
                console.log(new Date(e.xaxis.min) )
                }
            },
        },        
        colors: ['#563D7C','#25D366', '#34ABDF', '#FF567C'],
        dataLabels: {
            enabled: false
        },

        series: (typeof data == 'string')?JSON.parse(data):data,

        fill: {
            type: 'gradient',
            gradient: {
                opacityFrom: 0.6,
                opacityTo: 0.8,
            }
        },

        legend: {
            position: 'bottom',
            horizontalAlign: 'center',
            show: true,
            onItemHover: {
                highlightDataSeries: false,
            },
            offsetY: -10,
        },
        xaxis: {
            type: 'datetime',            
        },
        grid: {
            yaxis: {
                lines: {
                    show: true,
                },
                min:0
            },
            padding: {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            },
        },
        stroke: {
            show: true,
            curve: 'smooth',
            width: 2,
        },
    }

    var chart = new ApexCharts(
        document.querySelector(selector),
        options
    );
    chart.render();
    
}
