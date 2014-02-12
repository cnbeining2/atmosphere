define(['react', 'underscore', 'components/header', 'components/sidebar', 
        'components/footer', 'components/notifications', 'profile'],
function (React, _, Header, Sidebar, Footer, Notifications, profile) {

    var Application = React.createClass({
        getInitialState: function() {
            return {loading: true};
        },
        render: function() {
            /*
            var mainContent;
            if (this.state.loading)
                mainContent = React.DOM.div({className: 'loading'});
                */

            return React.DOM.div({},
                Header(),
                Sidebar(),
                Notifications(),
                React.DOM.div({'id': 'main'}),
                Footer()
            );
        }
    });

    return Application;
});
