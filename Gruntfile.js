module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            dist: {
                options: {
                    paths: [],
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapURL: '++resource++bda.plone.productshop.css.map',
                    sourceMapFilename: 'src/bda/plone/productshop/browser/resources/productshop_p5.css.map',
                    modifyVars: {
                        "isPlone": "false"
                    }
                },
                files: {
                    'src/bda/plone/productshop/browser/resources/productshop_p5.css': 'src/bda/plone/productshop/browser/resources/productshop_p5.less',
                }
            }
        },
        sed: {
            sed0: {
                path: 'src/bda/plone/productshop/browser/resources/productshop_p5.css.map',
                pattern: 'src/bda/plone/productshop/browser/resources/productshop_p5.less',
                replacement: '++resource++bda.plone.productshop.less',
            }
        },
        watch: {
            scripts: {
                files: ['src/bda/plone/productshop/browser/resources/productshop_p5.less'],
                tasks: ['less', 'sed']
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-sed');
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('compile', ['less', 'sed']);
};
