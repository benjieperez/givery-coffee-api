from tortoise import fields
from tortoise.models import Model


class Recipe(Model):
    id          = fields.IntField(pk=True)
    title       = fields.CharField(max_length=100)
    making_time = fields.CharField(max_length=100)
    serves      = fields.CharField(max_length=100)
    ingredients = fields.CharField(max_length=300)
    cost        = fields.IntField()
    created_at  = fields.DatetimeField(auto_now_add=True)
    updated_at  = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "recipes"

    def to_dict(self) -> dict:
        return {
            "id":           self.id,
            "title":        self.title,
            "making_time":  self.making_time,
            "serves":       self.serves,
            "ingredients":  self.ingredients,
            "cost":         self.cost,
            "created_at":   self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at":   self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }