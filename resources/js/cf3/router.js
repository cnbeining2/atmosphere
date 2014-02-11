define(['backbone'], function(Backbone) {
    var Router = Backbone.Router.extend({
        routes: {
            '': 'handleDefaultRoute',
            'dashboard': 'dashboard',
            'images': 'images',
            'instances': 'instances',
            'volumes': 'volumes',
            'providers': 'providers',
            'settings': 'settings',
            'help': 'help'
        },
        initialize: function(options) {
            this.app = options.app;
            this.defaultRoute = options.defaultRoute;
        },
        handleDefaultRoute: function() {
            this.toggleAppView(this.defaultRoute);
        },
        dashboard: function() {
            this.app.handleSelect("dashboard");
        },
        images: function() {
            this.app.handleSelect("images");
        },
        instances: function() {
            this.app.handleSelect("instances");
        },
        volumes: function() {
            this.app.handleSelect("volumes");
        },
        providers: function() {
            this.app.handleSelect("providers");
        },
        settings: function() {
            this.app.handleSelect("settings");
        },
        help: function() {
            this.app.handleSelect("help");
        }
    });

    return Router;
});
