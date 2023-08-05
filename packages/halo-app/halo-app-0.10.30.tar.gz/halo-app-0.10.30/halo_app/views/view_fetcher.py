from halo_app.app.uow import AbsUnitOfWork
from halo_app.classes import AbsBaseClass
from halo_app.views.query_filters import Filter


class AbsViewFetcher(AbsBaseClass):
    sql_query = ''
    dict_params = {}

    def set_sql_query(self):
        return self.sql_query

    def set_dict_params(self,params:dict,filters:[Filter]=None)->dict:
        return self.dict_params

    def query(self,params:dict,uow:AbsUnitOfWork,filters:[Filter]=None)->[dict]:
        sql_query = self.set_sql_query()
        self.set_dict_params(params,filters)
        with uow:
            results = list(uow.session.execute(sql_query,self.dict_params))
        return results

