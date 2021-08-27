from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.storage import is_valid_name


class IncStorage(AbstractSimpleTransformer):
    """
    Increments the value of a storage item by the specified value.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Increments the value of a storage item by the specified value."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="storage_name", value_type=str, def_value="var",
                                        help="The name of the storage item to increment"))
        self._option_manager.add(Option(name="inc_value", value_type=str, def_value="1",
                                        help="The value to increment the storage item by"))

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if self.storage_handler is None:
                result = "No storage handler available!"
        if result is None:
            name = self.get("storage_name")
            value = self.get("inc_value")
            if len(name) == 0:
                result = "No storage name provided!"
            elif not is_valid_name(name):
                result = "Not a valid storage name: %s" + name
            elif len(value) == 0:
                result = "No increment value provided!"
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        inc = self.get("inc_value")
        name = self.get("storage_name")
        if self.storage_handler.storage.has(name):
            value = self.storage_handler.storage.get(name)
        else:
            try:
                int(inc)
                value = 0
            except Exception:
                value = 0.0
        if isinstance(value, float):
            value_new = value + float(inc)
        else:
            value_new = value + int(inc)
        self.storage_handler.storage.set(name, value_new)
        if self.is_debug:
            self.log("Incremented storage: %s -> %s" % (str(value), str(value_new)))
        self._output.append(self._input)
        return None