from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from ryu.services.protocols.bgp import application as bgp_application


class MyBGPApp(app_manager.RyuApp):
    _CONTEXTS = {
        "ryubgpspeaker": bgp_application.RyuBGPSpeaker,
    }

    def __init__(self, *args, **kwargs):
        super(MyBGPApp, self).__init__(*args, **kwargs)

        # Stores "ryu.services.protocols.bgp.application.RyuBGPSpeaker"
        # instance in order to call the APIs of
        # "ryu.services.protocols.bgp.bgpspeaker.BGPSpeaker" via
        # "self.app.speaker".
        # Please note at this time, "BGPSpeaker" is NOT instantiated yet.
        self.app = kwargs["ryubgpspeaker"]

    @set_ev_cls(bgp_application.EventBestPathChanged)
    def _best_patch_changed_handler(self, ev):
        # self.logger.info("%s/%s", ev.path.nlri.addr,ev.path.nlri.length)
        # self.logger.info('%s',ev.path.next_path)
        pass
