define(['backbone', 'react'], function(Backbone, React) {
    var Router = Backbone.Router.extend({
        routes: {
            '': 'handleDefaultRoute',
            'dashboard': 'dashboard',
            'images': 'images',
            'images/favorites': 'imageFavorites',
            'images/authored': 'imageAuthored',
            'images/:id': 'imageDetail',
            'instances': 'instances',
            'volumes': 'volumes',
            'providers': 'providers',
            'settings': 'settings',
            'help': 'help'
        },
        setDefaultRoute: function(route) {
            this.defaultRoute = route;
        },
        handleDefaultRoute: function() {
            this.navigate(this.defaultRoute, {trigger: true, replace: true});
        },
        dashboard: function() {
            require(['components/dashboard'], function(Dashboard) {
                React.renderComponent(Dashboard(),
                    document.getElementById('main'));
            });
        },
        images: function() {
            require(['components/images'], function(Images) {
                React.renderComponent(Images(),
                    document.getElementById('main'));
            });
        },
        imageFavorites: function() {
        },
        imageAuthored: function() {
        },
        imageDetail: function() {
        },
        instances: function() {
            require(['components/instances'], function(Instances) {
                React.renderComponent(Instances(),
                    document.getElementById('main'));
            });
        },
        volumes: function() {
            require(['components/volumes'], function(Volumes) {
                React.renderComponent(Volumes(),
                    document.getElementById('main'));
            });
        },
        providers: function() {
            require(['components/providers'], function(Providers) {
                React.renderComponent(Providers(),
                    document.getElementById('main'));
            });
        },
        settings: function() {
            require(['components/settings'], function(Settings) {
                React.renderComponent(Settings(),
                    document.getElementById('main'));
            });
        },
        help: function() {
            require(['components/help'], function(Help) {
                React.renderComponent(Help(),
                    document.getElementById('main'));
            });
        }
    });

    return new Router();
});
