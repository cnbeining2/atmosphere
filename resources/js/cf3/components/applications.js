define(['react', 'underscore', 'components/page_header', 
    'collections/applications', 'components/common/gravatar'], 
    function(React, _, PageHeader, Applications, Gravatar) {

    var Rating = React.createClass({
        render: function() {
            var repeatString = function(string, num) {
                return new Array( num + 1 ).join( string );
            };
            return React.DOM.div({className: 'star-rating'}, 
                repeatString("\u2605", this.props.rating) + 
                repeatString("\u2606", 5 - this.props.rating));
        }
    });

    var ApplicationPreview = React.createClass({
        render: function() {
            var app = this.props.application;

            var icon;
            if (app.get('icon'))
                icon = React.DOM.img({
                    src: app.get('icon'),
                    width: 150,
                    height: 150
                });
            else
                icon = Gravatar({hash: app.get('uuid_hash'), size: 150});

            return React.DOM.li({}, 
                React.DOM.div({className: 'icon-container'}, icon),
                React.DOM.div({className: 'app-name'}, app.get('name_or_id')),
                Rating({rating: 4}));
        }
    });

    var ApplicationsHome = React.createClass({
        getInitialState: function() {
            return {
                applications: null
            };
        },
        helpText: function() {
            return React.DOM.p({}, "Applications are cool. You are, too. Keep bein' cool, bro.");
        },
        render: function() {
            var content = React.DOM.div({}, "loading");
            if (this.state.applications != null)
                content = React.DOM.ul({className: 'app-preview-list'}, this.state.applications.map(function(app) {
                    return ApplicationPreview({application: app});
                }));

            return React.DOM.div({},
                PageHeader({title: 'Apps', helpText: this.helpText}),
                content);
        },
        updateApplications: function(apps) {
            console.log(this);
            console.log(apps);
            this.setState({applications: apps});
        },
        componentDidMount: function() {
            var apps = new Applications();
            apps.on('sync', this.updateApplications);
            apps.fetch();
        },
        componentWillUnmount: function() {
            this.state.applications.off('sync', this.updateApplications);
        }
    });

    return ApplicationsHome;

});
